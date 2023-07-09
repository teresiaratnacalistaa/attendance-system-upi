import streamlit as st
from streamlit_option_menu import option_menu
import welcome, beranda, monitoring, rekap

st.set_page_config(
    page_title="Sistem Presensi Mahasiswa"
)

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, func):
        self.apps.append({
            "tittle": title,
            "function": func
        })
    def run():
        if 'username' not in st.session_state:
            st.session_state.username = ''
        if 'rolename' not in st.session_state:
            st.session_state.rolename = ''

        menu = ['Beranda']
        if st.session_state.rolename != '':
            if st.session_state.rolename == 'DOSEN':
                menu = ['Beranda','Rekap']
            if st.session_state.rolename == 'MAHASISWA':
                menu = ['Beranda','Monitoring','Rekap']

        with st.sidebar:
            app = option_menu(
                menu_title='Sistem Presensi Mahasiswa', 
                options=menu,
                icons=['house','clipboard-check','archive'],
                menu_icon='house-fill',
                default_index=0,
                styles={
                   "container": {"padding": "5!important","background-color":'black'},
                    "icons": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin":"0px", "--hoper-color": "blue"},
                    "nav-link-selected": {"background-color": "#FF5733"}, 
                }
            )

        if st.session_state.username != '':
            if app == "Beranda":
                beranda.app()
            if app == "Monitoring":
                monitoring.app()
            if app == "Rekap":
                rekap.app()
        else:
            st.warning('Silahkan login terlebih dahulu')
            welcome.app()
    
    run()