import streamlit as st
import welcome

def app():
    def s():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.rolename = ''

        if "signedout" not in st.session_state:
            st.session_state["signedout"] = False
        if 'signout' not in st.session_state:
            st.session_state['signout'] = False
        #welcome.app()

    if st.session_state.username != '':
        st.title('Selamat Datang di Sistem Presensi Mahasiswa')
        st.write("Sistem Presensi Online (SPO) merupakan program aplikasi presensi berbasis online bagi mahasiswa di lingkungan Universitas Pendidikan Indonesia (UPI)")
                
        st.write('Halo '+st.session_state.username+', yuk isi presensimu!')
        st.button('Sign Out', on_click=s)