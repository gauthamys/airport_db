import psycopg2
import streamlit as st 
import pandas as pd

def flightpage(new_user, pw):
    try:
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
        st.title("Flight Details")
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
            df=pd.DataFrame(
                counts,columns=['Airline ID','Flight ID','no of seats', 'Destination', 'gateno','Boarding Date','Boarding Time', 'Airline'])
            #st.dataframe(df)
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
            #end if;
        
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
        
        cur.close()
        con.close() 
    except:
        return
