'''APP'''
import psycopg2
import streamlit as st 
import pandas as pd
from passenger_db import delete_passenger_ssn
from sttrial import crewpage
from strunway import runwaypage

global ROLE
ROLE = 'casual'

def unique_user_page(us, pw):
    if us == 'admin':
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = 'postgres',
            password = pw
        )
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = us,
            password = pw
        )
    cur = con.cursor()
    if us == 'luggage_team':
        st.header('Unclaimed Luggage')
        cur.execute('with selected as (select * from luggage where picked=FALSE) select l_id,flight_id,firstnm,lastnm,phone,email from selected join passenger on pass_ssn=ssn;')
        f = cur.fetchall()
        f = pd.DataFrame(f)
        f.columns = ['Luggage ID', 'Flight ID', 'Passenger firtsname', 'Passenger Lastname', 'Phone', 'email']
        st.table(f)
    if us == 'scheduler':
        st.header('Flights that need to be assigned a runway')
        cur.execute('select * from flight where not exists (select * from runs_on where flight.flight_id=runs_on.flight_id)')
        f = cur.fetchall()
        f = pd.DataFrame(f).drop(columns=[3])
        f.columns=['Flight ID', 'Seats', 'Destination', 'Gate no', 'Boarding Date', 'Boarding Time']
        st.table(f)
        st.header('Runway Schedule')
        cur.execute('select runway_id, flight_id, destination, boarding_date, boarding_time from runs_on natural join flight order by boarding_date')
        s = cur.fetchall()
        s = pd.DataFrame(s, columns=['Runway', 'Flight ID', 'Destination', 'Date', 'Time'])
        st.table(s)


def passenger(new_user, pw):
    '''Passenger Table UI'''
    if new_user == 'admin':
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = 'postgres',
            password = pw
        )
    elif new_user == '':
        st.subheader('please choose a user to display')
        return
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = new_user,
            password = pw
        )
    st.header('Passengers')
    cur = con.cursor()
    try:
        cur.execute('select * from passenger')
        p = cur.fetchall()
        p = pd.DataFrame(p)
        p.columns=['ssn', 'First Name', 'Last Name', 'Phone', 'Email', 'Gender', 'Age', 'Class', 'Seat no.', 'Flight ID']
        tableref = st.empty()
        tableref.dataframe(p)
        form = st.radio('',['cancellations'])
        with st.container():
            if form == 'new booking':
                st.subheader('new booking')
                fname = st.text_input('', key='ins_fname', placeholder='passenger first name')
                st.button('confirm booking ?')
            
            if form == 'cancellations':
                st.subheader('cancellations')
                delid = st.selectbox('ssn of passenger to delete', key='delpass_ssn', options=p['ssn'])
                st.button('Delete ?', on_click=delete_passenger_ssn(delid, con))
            
            if form == 'update':
                st.subheader('update')
                st.button('update ?')
        return
    except psycopg2.errors.InsufficientPrivilege as e:
        st.write(f'insufficient permissions for user: {new_user}')
        st.error(e)
        return
    finally:
        cur.execute('select * from passenger;')
        p = cur.fetchall()
        p = pd.DataFrame(p)
        p.columns=['ssn', 'First Name', 'Last Name', 'Phone', 'Email', 'Gender', 'Age', 'Class', 'Seat no.', 'Flight ID']
        tableref.dataframe(p)
        cur.close()
        con.commit()
        con.close()

def crew(new_user, pw):
    #st.subheader('Crew')
    if new_user == 'admin':
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = 'postgres',
            password = pw
        )
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = new_user,
            password = pw
        )
    cur = con.cursor()
    try:
        crewpage(new_user, pw)
    except psycopg2.OperationalError as e:
        st.caption(str(e))
        return
    except psycopg2.errors.InsufficientPrivilege as e:
        st.error(f'{e}')
    finally:
        con.commit()
        cur.close()
        con.close()

def flight(new_user, pw):
    if new_user == 'admin':
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = 'postgres',
            password = pw
        )
    elif new_user == '':
        return
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = new_user,
            password = new_user
        )
    cur = con.cursor()
    st.title("Flight Details")
    try:
        with st.expander('View Flight Details'):
            cur.execute("select * from flight natural join airline order by boarding_date")
            counts=cur.fetchall()
            df=pd.DataFrame(
                counts,columns=['Airline ID','Flight ID','no of seats', 'Destination', 'gateno','Boarding Date','Boarding Time', 'Airline'])
            st.dataframe(df)

        with st.expander("Insert new flight details"):
            with st.form(key="f1",clear_on_submit=True):

                fid = st.text_input(label="flight_id")
                nseats = st.text_input(label='Enter no of seats')
                ddest = st.text_input(label='Enter destination')
                aid = st.text_input(label="Enter airline id")
                gno = st.text_input(label="Enter gateno")
                submit = st.form_submit_button(label="Submit")
                if fid and nseats and ddest and aid and gno:
                    record_to_insert = [fid,nseats,ddest,aid,gno]
                    cur.execute("INSERT INTO Flight VALUES(%s,%s,%s,%s,%s)", record_to_insert)
                    con.commit()
                    st.balloons()

        with st.expander("Update member details"):
            sql = "UPDATE FLIGHT"
            df=pd.DataFrame(counts,columns=['Airline ID','Flight ID','no of seats', 'Destination', 'gateno','Boarding Date','Boarding Time', 'Airline'])
            with st.form(key="f2",clear_on_submit=True):
                opt = st.selectbox("Which flight details would you like to update? ",df['Flight ID'])
                opt2 = st.selectbox('Select field to update',['Select','destination', 'airline_id', 'gateno'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
                if opt2 == 'destination':
                    cur.execute(sql+" SET destination='"+inp.split()[0]+"'where flight_id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                    con.commit()
                    st.balloons()
                if opt2 == 'airline_id':
                    cur.execute(sql+" SET airline_id='"+inp.split()[0]+"'where flight_id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                    con.commit()
                    st.balloons()
                if opt2 == 'gateno':
                    cur.execute(sql+" SET getno='"+inp.split()[0]+"'where flight_id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                    con.commit()
                    st.balloons()
        
        with st.expander('Delete flight data'):
            sql = "DELETE FROM FLIGHT"
            df=pd.DataFrame(
                counts,columns=['Airline ID','Flight ID','no of seats', 'Destination', 'gateno','Boarding Date','Boarding Time', 'Airline'])
            with st.form(key="f3",clear_on_submit=True):
                opt3 = st.selectbox("Which flight_id details do you want to delete?",[i for i in df['Flight ID']])
                submit4 = st.form_submit_button(label='Submit')
                if opt3 and submit4:
                    cur.execute(sql+' where flight_id='+str(opt3))
                    con.commit()
    except psycopg2.errors.InsufficientPrivilege as e:
        st.error(f'{e}')
    finally:
        cur.close()
        con.close()

def runway(new_user, pw):
    if new_user == 'admin':
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = 'postgres',
            password = pw
        )
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = new_user,
            password = pw
        )
    cur = con.cursor()
    try:
        runwaypage()
    except psycopg2.OperationalError as e:
        st.caption(e)
    finally:
        con.commit()
        cur.close()
        con.close()

def schedule():
    '''
        Landing page for flight schedule
        !!set password to your postgres user password!!
    '''
    con = psycopg2.connect(
        host = 'localhost',
        database = 'airport_db',
        user = 'postgres',
        password = 'gautham1234'
    )
    cur = con.cursor()
    cur.execute('select * from flight natural join airline order by boarding_date')
    sched = cur.fetchall()
    sched = pd.DataFrame(sched).drop(columns=[0, 2])
    sched.columns = ['Flight ID', 'Destination', 'Gate No.', 'Boarding Date', 'Boarding Time', 'Airline']
    #sched.columns = ['Destination', 'Airline']
    st.table(sched)
    cur.execute("select * from flight where destination='Bengaluru' or destination='Bangalore' order by boarding_date")
    inc = cur.fetchall()
    inc = pd.DataFrame(inc).drop(columns=[1, 3])
    inc.columns=['Flight ID', 'Destination', 'Gate no', 'Boarding Date', 'Arrival Time']
    st.header('Arrivals')
    st.table(inc)
    cur.execute("select * from flight where destination <> 'Bengaluru' or destination <> 'Bangalore' order by boarding_date;")
    dep = cur.fetchall()
    dep = pd.DataFrame(dep).drop(columns=[1, 3])
    dep.columns = ['Flight ID', 'Destination', 'Gate No', 'Boarding Date', 'Boarding Time']
    st.header('Departures')
    st.table(dep)
    cur.close()
    con.close()

def login(new_user, pw):
    '''Login using role new_user'''
    try:
        if new_user == 'admin':
            con = psycopg2.connect(
                host = 'localhost',
                database = 'airport_db',
                user = 'postgres',
                password = pw
            )
            con.close()
            st.sidebar.caption('\tlogged in as admin')
            st.balloons()
            return True
        
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = new_user,
            password = pw
        )
        ROLE = new_user
        st.sidebar.info('\tlogged in as ' + ROLE)
        con.close()
        st.balloons()
        return True
    except psycopg2.OperationalError as e:
        st.sidebar.warning('\tnot logged in')
        st.error(e)
        return False


title = st.container()
title.title('AIRPORT MANAGEMENT SYSTEM ✈️')
logref = st.container()
with st.sidebar.form(key='loginform', clear_on_submit=False):
    option = st.sidebar.selectbox('Choose user', options=('', 'security', 'admin', 'scheduler', 'luggage_team', 'security'), key='username')
    passw = st.sidebar.text_input('password',placeholder=f'enter password for {option}', type='password')
    st.sidebar.button('sign in', key='login')
ref = st.container()
page = st.sidebar.selectbox('Choose page', options=('home','flight', 'passenger', 'crew','runway'))
with ref:
    if passw == '' or option == '' :
        logref.subheader('please enter password and username')

    else:
        login(option, passw)
        try:
            if page == 'home':
                unique_user_page(option, passw)
                st.header('Flight Schedule')
                schedule()
            if page == 'flight':
                flight(option,passw)
            if page == 'passenger':
                passenger(option, passw)
            if page == 'crew':
                crew(option, passw)
            if page== 'runway':
                runway(option,passw)
        except psycopg2.errors.InFailedSqlTransaction as e:
            pass
        except psycopg2.OperationalError:
            pass
        except psycopg2.errors.InsufficientPrivilege:
            pass
