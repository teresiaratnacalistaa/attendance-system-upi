import cv2
import numpy as np
from numpy import array
import streamlit as st
import time
import pandas as pd
from PIL import Image, ImageOps 
from keras.models import load_model
from connect import connect
import psycopg2
import base64

def app():

    st.warning('Silahkan lakukan monitoring')
    st.title("Monitoring")

    conn = connect()
    cursor = conn.cursor()
    sql = "select \
        u.username, \
        k.namakelas, \
        m.namamatkul \
        from users u \
        join kelas k on k.userid = u.userid \
        join matkul m on m.idmatkul = k.idmatkul \
        join monitoring mo on mo.idkelas = k.idkelas \
        where u.userid = %s \
        and mo.tanggal = current_date ";
    cursor.execute(sql, (str(st.session_state.userid),))

    try:
        data = cursor.fetchall()
    except psycopg2.Error as e:
        print("Database error: " + e + "/n SQL: " + sql)
        
    iNama = st.selectbox("Nama", [st.session_state.username] if not data else [array(data)[0,0]])
    Kelas = st.selectbox("Kelas", [] if not data else array(data)[:,1])
    Matkul = st.selectbox("Mata Kuliah", [] if not data else array(data)[:,2])
    # Pertemuan = st.selectbox("Pertemuan", ["",
    #                                     "Pertemuan 1",
    #                                     "Pertemuan 2",
    #                                     "Pertemuan 3",
    #                                     "Pertemuan 4",
    #                                     "Pertemuan 5",
    #                                     "Pertemuan 6",
    #                                     "Pertemuan 7",
    #                                     "Pertemuan 8",
    #                                     "UAS"
    #                         ])
    Tanggal = st.date_input("Hari/tanggal", disabled=True)

    # CAMERA
    np.set_printoptions(suppress=True)
    #load model dan label
    model = load_model("kerasmodel.h5", compile=False) #model ml
    # model = load_model("kerasmodel_a128.h5", compile=False) #kelas a128
    # model = load_model("kerasmodel_b.h5", compile=False) #kelas b64
    class_names = open("labels.txt", "r").readlines()
    # class_names = open("labels_a128.txt", "r").readlines() #kelas a128
    # class_names = open("labels_b.txt", "r").readlines() #kelas b64
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    #load camera
    camera = st.camera_input("Bukti Kehadiran")
    if camera is not None:
        bytes_data = camera.getvalue()
        st.image(bytes_data)
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # resizing img to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image_PIL = Image.fromarray(cv2_img)
        image = ImageOps.fit(image_PIL, size, Image.Resampling.LANCZOS)

        # turn img into a numpy array
        image_array = np.asarray(image)

        # Normalize img
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the img into the array
        data[0] = normalized_image_array

        # Predicts model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        Akurasi = prediction[0][index]

        # Print prediction & confidence score
        namaakhir = class_name[2:]
        print("Class:", namaakhir, end="")
        print("Confidence Score:", Akurasi)

        if camera:
            progress_bar = st.progress(0)
            for perc_completed in range(100):
                time.sleep(0.05)
                progress_bar.progress(perc_completed+1)
            st.info(f"Wajah berhasil terdeteksi, {namaakhir}, {Akurasi}")

    submit = st.button("Submit")
    if submit:
        if iNama != "" and Kelas != "" and Matkul != "":
            if(iNama.lower().strip() == namaakhir.lower().strip()):
                sql = "select mo.idmonitoring, gambar, akurasi from monitoring mo join kelas k on k.idkelas = mo.idkelas join matkul m on m.idmatkul = k.idmatkul where m.active = 'T' and mo.tanggal = current_date and k.userid = %s and k.namakelas = %s and m.namamatkul = %s ";
                cursor.execute(sql, (str(st.session_state.userid),Kelas,Matkul))

                try:
                    monitoring = cursor.fetchone()
                    if monitoring[1] == None and monitoring[2] == None:
                        sql = "update monitoring set gambar = %s, akurasi = %s where idmonitoring = %s "
                        cursor.execute(sql, (base64.b64encode(bytes_data), str(Akurasi), monitoring[0]))
                        try:
                            conn.commit()
                            st.info("Presensi Sudah Masuk")
                        except psycopg2.Error as e:
                            print("Database error: " + str(e) + "/n SQL: " + sql)
                            st.warning("Tidak ada koneksi ke DB")
                    else:
                        st.warning("Sudah mengisi presensi, tidak bisa submit ulang")
                except psycopg2.Error as e:
                    print("Database error: " + str(e) + "/n SQL: " + sql)
                    st.warning("Tidak ada koneksi ke DB")
            else:
                st.warning("Tidak cocok, harap foto ulang")
        else:
            st.warning("Tidak ada pertemuan mata kuliah / kelas di hari ini")