import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np
import base64
from io import StringIO, BytesIO
from connect import connect
import psycopg2

def generate_excel_download_link(dfi):
    towrite = BytesIO()
    dfi.to_excel(towrite, encoding="utf-8", index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download File Rekap</a>'
    return st.markdown(href, unsafe_allow_html=True)

def app():
    st.markdown("<h1 style='text-align:center;'>Rekap Monitoring\n\nSemester Genap 2022/2023</h1>", unsafe_allow_html=True)
    
    conn = connect()
    cursor = conn.cursor()

    sqlKelas = "select k.idmatkul, m.namamatkul, u.username, k.semester, k.namakelas \
        from kelas k \
        join matkul m on m.idmatkul = k.idmatkul \
        join users u on u.userid = k.dosenid \
        where k.userid = %s \
        group by k.idmatkul, m.namamatkul, u.username, k.semester, k.namakelas ";
    cursor.execute(sqlKelas, (str(st.session_state.userid),))

    try:
        kelasL = cursor.fetchall()
    except psycopg2.Error as e:
        print("Database error: " + e + "/n SQL: " + sqlKelas)

    for kelas in kelasL:
        col1, col2= st.columns(2)
        with col1:
            st.write("Mata Kuliah : " + kelas[1])
            st.write("Nama Dosen : " + kelas[2])
        with col2:
            st.write("Semester : " + kelas[3])
            st.write("Kelas : " + kelas[4])

        sql = "select u.username,  \
            case when m1.gambar is not null and m1.akurasi is not null then true else false end as p1, \
            case when m2.gambar is not null and m2.akurasi is not null then true else false end as p2, \
            case when m3.gambar is not null and m3.akurasi is not null then true else false end as p3, \
            case when m4.gambar is not null and m4.akurasi is not null then true else false end as p4, \
            case when m5.gambar is not null and m5.akurasi is not null then true else false end as p5, \
            case when m6.gambar is not null and m6.akurasi is not null then true else false end as p6, \
            case when m7.gambar is not null and m7.akurasi is not null then true else false end as p7, \
            case when m8.gambar is not null and m8.akurasi is not null then true else false end as p8, \
            case when m9.gambar is not null and m9.akurasi is not null then true else false end as p9, \
            case when m10.gambar is not null and m10.akurasi is not null then true else false end as p10, \
            mc.jum as jumlah \
            from kelas k \
            join users u on u.userid = k.userid \
            join matkul m on m.idmatkul = k.idmatkul \
            join monitoring m1 on m1.idkelas = k.idkelas and m1.pertemuan = 'Pertemuan 1' \
            join monitoring m2 on m2.idkelas = k.idkelas and m2.pertemuan = 'Pertemuan 2' \
            join monitoring m3 on m3.idkelas = k.idkelas and m3.pertemuan = 'Pertemuan 3' \
            join monitoring m4 on m4.idkelas = k.idkelas and m4.pertemuan = 'Pertemuan 4' \
            join monitoring m5 on m5.idkelas = k.idkelas and m5.pertemuan = 'Pertemuan 5' \
            join monitoring m6 on m6.idkelas = k.idkelas and m6.pertemuan = 'Pertemuan 6' \
            join monitoring m7 on m7.idkelas = k.idkelas and m7.pertemuan = 'Pertemuan 7' \
            join monitoring m8 on m8.idkelas = k.idkelas and m8.pertemuan = 'Pertemuan 8' \
            join monitoring m9 on m9.idkelas = k.idkelas and m9.pertemuan = 'Pertemuan 9' \
            join monitoring m10 on m10.idkelas = k.idkelas and m10.pertemuan = 'Pertemuan 10' \
            join ( \
                select idkelas, \
                sum(case when gambar is not null and akurasi is not null then 1 else 0 end) as jum \
                from monitoring \
                group by idkelas \
            ) mc on mc.idkelas = k.idkelas \
            where u.active = 'T' and m.active = 'T' \
            and k.namakelas = %s \
            and k.idmatkul = %s ";

        #T = True F= False
        sql += "order by u.username ";
        cursor.execute(sql, (kelas[4],str(kelas[0])))

        try:
            result = cursor.fetchall()
        except psycopg2.Error as e:
            print("Database error: " + e + "/n SQL: " + sql)
        print(result)
        df = pd.DataFrame(result, columns=['Nama Mahasiswa', 'Pertemuan 1', 'Pertemuan 2', 'Pertemuan 3', 'Pertemuan 4', 'Pertemuan 5', 'Pertemuan 6', 'Pertemuan 7', 'Pertemuan 8', 'Pertemuan 9', 'Pertemuan 10', 'Jumlah'])
        df.index = np.arange(1, len(df) + 1)
        st.dataframe(df)
        generate_excel_download_link(df)
        st.markdown('******')
        