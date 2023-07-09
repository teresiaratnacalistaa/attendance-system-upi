import streamlit as st
import beranda
from connect import connect
import psycopg2

def app():
    def f():
        cursor = None
        conn = None
        try:
            conn = connect()
            cursor = conn.cursor()
            sql = "select userid, username, rolename from users where username = %s and password = %s and active = 'T' "
            cursor.execute(sql, (username, password))
            try:
                user = cursor.fetchone()
            except psycopg2.Error as e:
                print("Database error: " + e + "/n SQL: " + sql)

            st.session_state.userid = user[0]
            st.session_state.username = user[1]
            st.session_state.rolename = user[2]

            st.session_state.signedout = True
            st.session_state.signout = True
            #beranda.app()
        except:
            st.warning('Login Failed')
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
        
    def t():
        try:
            conn = connect()
            cursor = conn.cursor()
            sql = "insert into users(userid, username, password, rolename) values(nextval('user_seq'), %s, %s, 'MAHASISWA') "
            cursor.execute(sql, (username, password))
            try:
                conn.commit()
            except psycopg2.Error as e:
                print("Database error: " + e + "/n SQL: " + sql)
        except:
            st.warning('Create Account Failed')
        finally:
            cursor.close()
            conn.close()
        st.success('Account created successfully')
        st.markdown('Please Login using your username and password')
        st.balloons()

    if st.session_state.username == '':
        st.title('Selamat Datang di Sistem Presensi Mahasiswa')
        choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])
        if choice=='Login':
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=f)
        else:
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            st.button('Create your account', on_click=t)