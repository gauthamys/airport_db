import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 

def crewpage(us, pw):
    if us == 'admin':
        con = psycopg2.connect(
            host = "localhost",
            database="airport_db",
            user="postgres",
            password="gautham1234"
        )
    else:
        con = psycopg2.connect(
            host = 'localhost',
            database = 'airport_db',
            user = us,
            password = pw
        )
        
    cur=con.cursor()

    def deletepage(option,counts,sql):
        with st.form(key=option[0]+option[1]+'3',clear_on_submit=True):
            opt = st.selectbox("Which entry do you want to delete?",[i for i in counts])
            submit = st.form_submit_button(label='Submit')
        cur.execute(sql+' where id='+str(opt[0]))
        con.commit()
    st.title("Crew Member Details")
    st.header("Department")
    st.sidebar.write("Sidebar")
    option = st.sidebar.selectbox("Which Department?", ('Cabin crew','Ground','Security Team','Service','Operations'))
    st.subheader(option)

    if option=='Ground':
        with st.expander('View Details'):
            cur.execute("select * from crew where dept='Ground'")
            counts=cur.fetchall()
            for i in counts:
                st.write(i)
            df=pd.DataFrame(
                counts,columns=['id','First Name','Last Name', 'Age', 'SSN', 'Gender','Gate No','Department'])
            st.dataframe(df)

        with st.expander("Insert new member details"):
            with st.form(key="Groundins",clear_on_submit=True):

                idd = st.text_input(label="id")
                fname = st.text_input(label='Enter First Name')
                lname = st.text_input(label='Enter Last Name')
                age = st.text_input(label="Enter Age")
                SSN = st.text_input(label="Enter SSN")
                gender  = st.selectbox("Select Gender",['Select','F','M','Prefer Not to Say'])
                gateno = st.selectbox("Select Gate",['Select','1','2','3','4','5','6','7','8'])
                deptt="Ground"
                submit = st.form_submit_button(label="Submit")
            if fname and lname and age and SSN and gender!='Select' and gateno!='Select' and deptt:
                record_to_insert = [idd,fname,lname,age,SSN,gender,gateno,deptt]
                cur.execute("INSERT INTO CREW VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", record_to_insert)
                con.commit()
                st.balloons()

        with st.expander("Update member details"):
            sql = "UPDATE CREW"
            with st.form(key="G2",clear_on_submit=True):
                opt = st.selectbox("What would you like to update?",[i for i in counts])
                opt2 = st.selectbox('Select field to update',['Select','Name','Age','SSN','GateNo','Dept'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
            if opt2 == 'Name':
                cur.execute(sql+" SET fname='"+inp.split()[0]+"' ,lname='"+inp.split()[1]+"'where id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                con.commit()
                st.balloons()
            elif opt2!='Select' and inp:
                if type(inp)==str:
                    cur.execute(sql+" SET "+opt2+"='"+str(inp)+"' where id="+str(opt[0]),(str(inp),(opt[0])))
                else:
                    cur.execute(sql+" SET "+opt2+"="+str(inp)+" where id="+str(opt[0]),(str(inp),(opt[0])))
                con.commit()
                st.balloons()
        
        with st.expander('Delete member data'):
            sql = "DELETE FROM CREW"
            with st.form(key=option[0]+option[1]+'3',clear_on_submit=True):
                opt3 = st.selectbox("Which entry do you want to delete?",[i for i in counts])
                submit = st.form_submit_button(label='Submit')
            cur.execute(sql+' where id='+str(opt3[0]))
            con.commit()

    if option=='Cabin crew':
        with st.expander('View Details'):
            cur.execute("select * from pilot")
            counts=cur.fetchall()
            df=pd.DataFrame(
                counts,columns=[ 'Pid','First Name','Last Name','Age','Pssn','Gender','Salary','Status','Airline_id','Flight_id'])
            st.dataframe(df)

        with st.expander("Insert new member details"):
            with st.form(key="Cabinins",clear_on_submit=True):

                idd = st.text_input(label="id")
                fname = st.text_input(label='Enter First Name')
                lname = st.text_input(label='Enter Last Name')
                age = st.text_input(label="Enter Age")
                pSSN = st.text_input(label="Enter SSN")
                gender  = st.selectbox("Select Gender",['Select','F','M','Prefer Not to Say'])
                Salary = st.text_input(label="Enter Salary")
                status=st.text_input(label='Enter Status')
                airlinei = st.selectbox("Select Airline",['Select','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
                flighti = st.selectbox("Select Flight id",['Select','221122112','334433443','556655665','778877887','987654321','111111111','222222222','333333333','444444444','555555555','123456789','112211221','111111112','111111113','111111114'])
                submit = st.form_submit_button(label="Submit")
            if idd and fname and lname and age and pSSN and gender!='Select' and Salary and status and airlinei!='Select' and flighti!='Select':
                record_to_insert = [idd,fname,lname,age,pSSN,gender,Salary,status,airlinei,flighti]
                cur.execute("INSERT INTO PILOT VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", record_to_insert)
                con.commit()
                st.balloons()

        with st.expander("Update member details"):
            sql = "UPDATE PILOT"
            with st.form(key="C2",clear_on_submit=True):
                opt = st.selectbox("What would you like to update?",[i for i in counts])
                opt2 = st.selectbox('Select field to update',['Select','Name','Age','pSSN','Salary','Status','Airline_id','Flight_id'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
            if opt2 == 'Name':
                cur.execute(sql+" SET fname='"+inp.split()[0]+"' ,lname='"+inp.split()[1]+"'where pid="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                con.commit()
                st.balloons()
            elif opt2!='Select' and inp:
                if type(inp)==str:
                    cur.execute(sql+" SET "+opt2+"='"+str(inp)+"' where pid="+str(opt[0]),(str(inp),(opt[0])))
                else:
                    cur.execute(sql+" SET "+opt2+"="+str(inp)+" where pid="+str(opt[0]),(str(inp),(opt[0])))
                con.commit()
                st.balloons()
        
        with st.expander('Delete member data'):
            sql = "DELETE FROM PILOT"
            with st.form(key='P3',clear_on_submit=True):
                opt3 = st.selectbox("Which entry do you want to delete?",[i for i in counts])
                submit3 = st.form_submit_button(label='Submit')
            if opt3 and submit3:
                cur.execute(sql+' where pid='+str(opt3[0]))
                con.commit()

    if option=='Security Team':
        with st.expander('View Details'):
            cur.execute("select * from crew where dept='Security Team'")
            counts=cur.fetchall()
            df=pd.DataFrame(
                counts,columns=['id','First Name','Last Name', 'Age', 'SSN', 'Gender','Gate No','Department'])
            st.dataframe(df)

        with st.expander("Insert new member details"):
            with st.form(key="Securins",clear_on_submit=True):

                idd = st.text_input(label="id")
                fname = st.text_input(label='Enter First Name')
                lname = st.text_input(label='Enter Last Name')
                age = st.text_input(label="Enter Age")
                SSN = st.text_input(label="Enter SSN")
                gender  = st.selectbox("Select Gender",['Select','F','M','Prefer Not to Say'])
                gateno = st.selectbox("Select Gate",['Select','1','2','3','4','5','6','7','8'])
                deptt="Security Team"
                submit = st.form_submit_button(label="Submit")
            if fname and lname and age and SSN and gender!='Select' and gateno!='Select' and deptt:
                record_to_insert = [idd,fname,lname,age,SSN,gender,gateno,deptt]
                cur.execute("INSERT INTO CREW VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", record_to_insert)
                con.commit()
                st.balloons()

        with st.expander("Update member details"):
            sql = "UPDATE CREW"
            with st.form(key="S2",clear_on_submit=True):
                opt = st.selectbox("What would you like to update?",[i for i in counts])
                opt2 = st.selectbox('Select field to update',['Select','Name','Age','SSN','GateNo','Dept'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
            if opt2 == 'Name':
                cur.execute(sql+" SET fname='"+inp.split()[0]+"' ,lname='"+inp.split()[1]+"'where id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                con.commit()
                st.balloons()
            elif opt2!='Select' and inp:
                if type(inp)==str:
                    cur.execute(sql+" SET "+opt2+"='"+str(inp)+"' where id="+str(opt[0]),(str(inp),(opt[0])))
                else:
                    cur.execute(sql+" SET "+opt2+"="+str(inp)+" where id="+str(opt[0]),(str(inp),(opt[0])))
                con.commit()
                st.balloons()
        
        with st.expander('Delete member data'):
            sql = "DELETE FROM CREW"
            with st.form(key=option[0]+option[1]+'4',clear_on_submit=True):
                opt3 = st.selectbox("Which entry do you want to delete?",[i for i in counts])
                submit = st.form_submit_button(label='Submit')
            cur.execute(sql+' where id='+str(opt3[0]))
            con.commit()

    if option=='Service':
        with st.expander('View Details'):
            cur.execute("select * from crew where dept='Service'")
            counts=cur.fetchall()
            df=pd.DataFrame(
                counts,columns=['id','First Name','Last Name', 'Age', 'SSN', 'Gender','Gate No','Department'])
            st.dataframe(df)
        with st.expander("Insert new member details"):
            with st.form(key="Servins",clear_on_submit=True):

                idd = st.text_input(label="id")
                fname = st.text_input(label='Enter First Name')
                lname = st.text_input(label='Enter Last Name')
                age = st.text_input(label="Enter Age")
                SSN = st.text_input(label="Enter SSN")
                gender  = st.selectbox("Select Gender",['Select','F','M','Prefer Not to Say'])
                gateno = st.selectbox("Select Gate",['Select','1','2','3','4','5','6','7','8'])
                deptt="Service"
                submit = st.form_submit_button(label="Submit")
            if fname and lname and age and SSN and gender!='Select' and gateno!='Select' and deptt:
                record_to_insert = [idd,fname,lname,age,SSN,gender,gateno,deptt]
                cur.execute("INSERT INTO CREW VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", record_to_insert)
                con.commit()
                st.balloons()
        with st.expander("Update member details"):
            sql = "UPDATE CREW"
            with st.form(key="Serv2",clear_on_submit=True):
                opt = st.selectbox("What would you like to update?",[i for i in counts])
                opt2 = st.selectbox('Select field to update',['Select','Name','Age','SSN','GateNo','Dept'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
            if opt2 == 'Name':
                cur.execute(sql+" SET fname='"+inp.split()[0]+"' ,lname='"+inp.split()[1]+"'where id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                con.commit()
                st.balloons()
            elif opt2!='Select' and inp:
                if type(inp)==str:
                    cur.execute(sql+" SET "+opt2+"='"+str(inp)+"' where id="+str(opt[0]),(str(inp),(opt[0])))
                else:
                    cur.execute(sql+" SET "+opt2+"="+str(inp)+" where id="+str(opt[0]),(str(inp),(opt[0])))
                con.commit()
                st.balloons()
        with st.expander('Delete member data'):
            sql = "DELETE FROM CREW"
            with st.form(key='Ser3',clear_on_submit=True):
                opt3 = st.selectbox("Which entry do you want to delete?",[i for i in counts])
                submit3 = st.form_submit_button(label='Submit')
            cur.execute(sql+' where id='+str(opt3[0]))
            con.commit()

    if option=='Operations':
        with st.expander('View Details'):
            cur.execute("select * from crew where dept='Operations'")
            counts=cur.fetchall()
            df=pd.DataFrame(
                counts,columns=['id','First Name','Last Name', 'Age', 'SSN', 'Gender','Gate No','Department'])
            st.dataframe(df)
        
        with st.expander("Insert new member details"):
            with st.form(key="Operins",clear_on_submit=True):

                idd = st.text_input(label="id")
                fname = st.text_input(label='Enter First Name')
                lname = st.text_input(label='Enter Last Name')
                age = st.text_input(label="Enter Age")
                SSN = st.text_input(label="Enter SSN")
                gender  = st.selectbox("Select Gender",['Select','F','M','Prefer Not to Say'])
                gateno = st.selectbox("Select Gate",['Select','1','2','3','4','5','6','7','8'])
                deptt="Operations"
                submit = st.form_submit_button(label="Submit")
            if fname and lname and age and SSN and gender!='Select' and gateno!='Select' and deptt:
                record_to_insert = [idd,fname,lname,age,SSN,gender,gateno,deptt]
                cur.execute("INSERT INTO CREW VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", record_to_insert)
                con.commit()
                st.balloons()

        with st.expander("Update member details"):
            sql = "UPDATE CREW"
            with st.form(key="O2",clear_on_submit=True):
                opt = st.selectbox("What would you like to update?",[i for i in counts])
                opt2 = st.selectbox('Select field to update',['Select','Name','Age','SSN','GateNo','Dept'])
                inp = st.text_input(label='Enter the new value')
                submit2 = st.form_submit_button(label='Submit')
            if opt2 == 'Name':
                cur.execute(sql+" SET fname='"+inp.split()[0]+"' ,lname='"+inp.split()[1]+"'where id="+str(opt[0]),(inp.split()[0],inp.split()[1],(opt[0])))
                con.commit()
                st.balloons()
            elif opt2!='Select' and inp:
                if type(inp)==str:
                    cur.execute(sql+" SET "+opt2+"='"+str(inp)+"' where id="+str(opt[0]),(str(inp),(opt[0])))
                else:
                    cur.execute(sql+" SET "+opt2+"="+str(inp)+" where id="+str(opt[0]),(str(inp),(opt[0])))
                con.commit()
                st.balloons()
        with st.expander('Delete member data'):
            sql = "DELETE FROM CREW"
            with st.form(key='O3',clear_on_submit=True):
                opt3 = st.selectbox("Which entry do you want to delete?",[i for i in counts])
                submit3 = st.form_submit_button(label='Submit')
            cur.execute(sql+' where id='+str(opt3[0]))
            con.commit()

    cur.close()
    con.close() 