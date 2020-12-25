from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from flask_restful import Resource, Api
from datetime import datetime
import random
import os
import pathlib
from werkzeug.utils import secure_filename
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model

from app_utils import features_extraction_with_mfcc_test, predict_speech_recognition, predict_speaker_verification

# tf.logging.set_verbosity(tf.logging.ERROR) # hide warning

UPLOAD_FOLDER = './voices'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Untuk buat API
api = Api(app)

# untuk model deep learning
model_sr = None
model_sv = None

# graph = tf.get_default_graph()

# Untuk koneksi ke database MySQL di phpmyadmin
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web_flask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # dipake supaya pas fetch data bisa pake nama kolom db
mysql = MySQL(app)

# Halaman Index
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT attempt, nama_rekaman_transaksi, kode_angka, path_rekaman, y_pred_sv, y_pred_sr FROM rekaman_transaksi WHERE id_transaksi='TRS340471'")
    fetch_data = cur.fetchall()
    cur.close()

    return render_template('index.html', data = fetch_data)

# Halaman Dasbor
@app.route('/dasbor')
def dasbor():
    cur = mysql.connection.cursor()
    str_sql = ('SELECT t.id_transaksi, t.waktu_transaksi, u.nama_user, po.nama_provider, pu.nominal_pulsa, t.no_hp, t.status_transaksi ' +
                'FROM transaksi t JOIN user u ON (t.id_user = u.id_user) ' +
                'JOIN provider po ON (t.nama_provider = po.nama_provider) ' +
                'JOIN pulsa pu ON (t.nominal_pulsa = pu.nominal_pulsa) ORDER BY t.waktu_transaksi DESC')
    cur.execute(str_sql)

    data_transaksi = cur.fetchall()
    cur.close()

    return render_template('dasbor.html', data = data_transaksi)

# Halaman Detail Transaksi
@app.route('/detail_transaksi/<id_transaksi>')
def detail_transaksi(id_transaksi):
    cur = mysql.connection.cursor()
    str_sql = ("SELECT t.id_transaksi, t.waktu_transaksi, u.nama_user, po.nama_provider, pu.nominal_pulsa, t.no_hp, "
                + "t.status_transaksi FROM transaksi t JOIN user u ON (t.id_user = u.id_user) "
                + "JOIN provider po ON (t.nama_provider = po.nama_provider) "
                + "JOIN pulsa pu ON (t.nominal_pulsa = pu.nominal_pulsa) WHERE t.id_transaksi='" + id_transaksi + "'")
    cur.execute(str_sql)

    detail_transaksi = cur.fetchall()

    sql_detil = ("SELECT attempt, nama_rekaman_transaksi, kode_angka, path_rekaman, y_pred_sv, y_pred_sr FROM rekaman_transaksi WHERE id_transaksi='"+ id_transaksi +"'")
    cur.execute(sql_detil)

    audio = cur.fetchall()

    cur.close()

    return render_template('detail_transaksi.html', data=detail_transaksi[0], audio=audio)

@app.route('/play_audio/', methods=['GET'])
def play_audio():
    path_rekaman =  request.args.get('path_rekaman')
    nama_file =  request.args.get('nama_file')

    string = './' + nama_file
    path_rekaman_fix = path_rekaman.replace(string, '')

    return send_from_directory(path_rekaman_fix, nama_file)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------------------------------------------------------

# Api untuk Session
class session(Resource):
    def post(self):
        # ambil data login dari request JSON
        req_json = request.get_json()
        # ambil email dan password dari request JSON
        email = req_json['email']
        password = req_json['password']

        cur = mysql.connection.cursor()
        str_sql= "SELECT id_user, password_user, status_pendaftaran_suara FROM user WHERE email_user='" + email +"'"
        cur.execute(str_sql)

        data = cur.fetchall()
        cur.close()

        # cek dulu data < 1 atau ngga
        if(len(data) == 0):
            res_json = {
                'response_msg' : 'Akun tidak terdaftar',
                'response_code' : -1401
            }
        else: # kalo bener data nya 1 baris
            data = data[0]

            # cek sekali lagi akunnya aktif atau ngga
            status = data['status_pendaftaran_suara']
            if(status == 0):
                res_json = {
                    'response_msg' : 'Akun tidak terdaftar',
                    'response_code' : -1401
                }  
                return res_json 

            # baru lanjut cek password
            # cocokin password request sama yg di db
            password_db = data['password_user']
            if(password == password_db): 
                res_json = {
                    'session':[{
                        'id_user' : data['id_user']
                    }],
                    'response_msg' : 'OK',
                    'response_code' : 0
                }
            else:
                res_json = {
                    'response_msg' : 'Gagal Login',
                    'response_code' : -1402
                }
        return res_json

# Api untuk userss
class users(Resource):
    def get(self, id_user):
        # ambil data dari req json
        # req_json = request.get_json()
        # id_user = id_user

        cur = mysql.connection.cursor()
        str_sql= ("SELECT id_user, nama_user, email_user, no_hp_user, password_user, saldo_user FROM user WHERE id_user='"+ id_user +"'")
        cur.execute(str_sql)

        data = cur.fetchall()
        cur.close()

        if(len(data) == 0):
            res_json = {
                'response_msg' : 'Akun tidak terdaftar',
                'response_code' : -1401
            }
        else:
            data = data[0]
            res_json = {
                'user':[{
                    'id_user':data['id_user'],
                    'nama_user':data['nama_user'],
                    'email_user':data['email_user'],
                    'no_hp_user':data['no_hp_user'],
                    'password_user':data['password_user'],
                    'saldo_user':data['saldo_user'],
                }],
                'response_msg' : 'OK',
                'response_code' : 0
            }
            # print(res_json)
        return res_json
    def post(self):
        req_json = request.get_json()

        id_user = req_json['id_user']
        nama_user_baru = req_json['nama_user']
        email_user_baru = req_json['email_user']
        no_hp_user_baru = req_json['no_hp_user']
        password_user = req_json['password_user']

        # cek dulu udah ada belum email dan no telp nya
        cur = mysql.connection.cursor()
        cek_email_sql = ("SELECT email_user FROM user WHERE email_user ='" + email_user_baru +"'")
        cur.execute(cek_email_sql)
        hasil_email = cur.fetchall()

        cek_nohp_sql = ("SELECT no_hp_user FROM user WHERE no_hp_user='"+ no_hp_user_baru +"'")
        cur.execute(cek_nohp_sql)
        hasil_nohp = cur.fetchall()
        cur.close()

        if(len(hasil_email) > 0 and len(hasil_nohp) == 0): # kalo email uda terdaftar tp no hp ngga
            res_json = {
                'response_msg' : 'Email telah terdaftar. Gunakan email lain',
                'response_code' : -1406
            }
        elif(len(hasil_email) == 0 and len(hasil_nohp) > 0): # kalo no hp udah terdaftar tp email ngga
            res_json = {
                'response_msg' : 'Nomor Handphone telah terdaftar. Gunakan nomor handphone lain',
                'response_code' : -1407
            }
        elif(len(hasil_email) > 0 and len(hasil_nohp) > 0): # kalo no hp dan email ud terdaftar
            res_json = {
                'response_msg' : 'Nomor Handphone dan email telah terdaftar. Gunakan nomor handphone dan email lain',
                'response_code' : -1408
            }
        else:
            cur = mysql.connection.cursor()
            result = cur.execute("INSERT INTO user (id_user, nama_user, email_user, password_user, no_hp_user) VALUES(%s, %s, %s, %s, %s)", (id_user, nama_user_baru, email_user_baru, password_user, no_hp_user_baru))
            cur.close()
            mysql.connection.commit()

            if(result):
                res_json = {
                    'response_msg' : 'OK',
                    'response_code' : 0
                }
            else:
                res_json = {
                    'response_msg' : 'Gagal menambahkan user',
                    'response_code' : -1405
                }
        
        return res_json
    def delete(self, id_user):
        id_user = id_user
        cur = mysql.connection.cursor()
        result = cur.execute("DELETE FROM user WHERE id_user=%s", [id_user])
        cur.close()
        mysql.connection.commit()

        if(result):
            res_json = {
                'response_msg' : 'OK',
                'response_code' : 0

            }
        else:
            res_json = {
                'response_msg' : 'Gagal menghapus akun',
                'response_code' : -1413
            }
        return res_json

class user_profile(Resource):
    def patch(self, id_user):
        # ambil data dari req json
        req_json = request.get_json()

        id_user = id_user
        nama_user_baru = req_json['nama_user']
        email_user_baru = req_json['email_user']
        no_hp_user_baru = req_json['no_hp_user']

        cur = mysql.connection.cursor()
        result = cur.execute("UPDATE user SET nama_user=%s, email_user=%s, no_hp_user=%s WHERE id_user=%s", (nama_user_baru, email_user_baru, no_hp_user_baru, id_user))
        cur.close()
        mysql.connection.commit()

        # print("UPDATE user SET nama_user=%s, email_user=%s, no_hp_user=%s WHERE id_user=%s", (nama_user_baru, email_user_baru, no_hp_user_baru, id_user))

        if(result):
            res_json = {
                'response_msg' : 'OK',
                'response_code' : 0

            }
        else:
            res_json = {
                'response_msg' : 'Gagal update profile',
                'response_code' : -1403
            }
        return res_json

class user_password(Resource):
    def patch(self, id_user):
        # ambil data dari req json
        req_json = request.get_json()

        id_user = id_user
        password_baru = req_json['password_user']

        cur = mysql.connection.cursor()
        result = cur.execute("UPDATE user SET password_user=%s WHERE id_user=%s", (password_baru, id_user))
        cur.close()
        mysql.connection.commit()

        if(result):
            res_json = {
                'response_msg' : 'OK',
                'response_code' : 0
            }
        else:
            res_json = {
                'response_msg' : 'Gagal update password',
                'response_code' : -1404
            }
        return res_json

class user_active(Resource):
    def patch(self, id_user):
        # ambil data dari req json
        req_json = request.get_json()

        id_user = id_user
        status_daftar = req_json['status_pendaftaran_suara']

        try:
            # dapatkan path folder id_user yang berisi audio yang telah diupload
            path_folder_user = os.path.join(app.config['UPLOAD_FOLDER'], 'users', id_user)
            
            count_file = len([name for name in os.listdir(path_folder_user) if os.path.isfile(os.path.join(path_folder_user, name))])

            if(count_file < 9):
                return {
                    'response_code' : -1544,
                    'response_msg' : 'Gagal menggunduh rekaman suara user'
                }
        except Exception as e:
            return {
                'response_code' : -1544,
                'response_msg' : 'Gagal menggunduh rekaman suara user'
            }
        # kalo uda bener ada 9 rekaman baru ekstraksi fitur
        
        # features extraction juga
        path_npz = features_extraction_with_mfcc_test(path_folder_user, '/', id_user)
        path_npz += '.npz'
        
        cur = mysql.connection.cursor()
        result = cur.execute("UPDATE user SET status_pendaftaran_suara=%s, path_mfcc=%s WHERE id_user=%s", (status_daftar, path_npz, id_user))
        cur.close()
        mysql.connection.commit()

        if(result):
            res_json = {
                'response_msg' : 'OK',
                'response_code' : 0
            }
        else:
            res_json = {
                'response_msg' : 'Gagal mengaktifkan akun',
                'response_code' : -1410
            }
        return res_json

class transactions(Resource):
    def get(self, id_user):
        cur = mysql.connection.cursor()
        str_sql = ("SELECT id_transaksi, nama_provider, nominal_pulsa, status_transaksi, waktu_transaksi, no_hp " +
                    "FROM transaksi " +
                    "WHERE id_user = '"+ id_user +"'")
        cur.execute(str_sql)
        data = cur.fetchall()
        cur.close()

        if(len(data) == 0):
            res_json = {
                'response_msg' : 'Tidak ada data transaksi',
                'response_code' : -1409
            }
        else:
            data_array = []
            
            for row in data:
                data_dict = {}
                attributes = list(row.keys())
                for attr in attributes:
                    # kalo datetime diconvert dlu jadi string
                    if(attr == 'waktu_transaksi'):
                        d = row[attr]
                        data_dict[attr] = d.strftime("%d %b, %Y")
                        # print(data_dict[attr])
                    # selain datetime
                    else: 
                        data_dict[attr] = row[attr]
                data_array.append(data_dict)
                
            # print(data_array)

            res_json = {
                'transactions' : data_array,
                'response_code' : 0,
                'response_msg' : 'OK'
            }

        return res_json
    def post(self):
        req_json = request.get_json()

        id_transaksi = req_json['id_transaksi']
        id_user = req_json['id_user']
        nama_provider = req_json['nama_provider']
        no_hp = req_json['no_hp']
        nominal_pulsa = int(req_json['nominal_pulsa'])

        cur = mysql.connection.cursor()
        result = cur.execute("INSERT INTO transaksi (id_transaksi, id_user, no_hp, nama_provider, nominal_pulsa) VALUES(%s, %s, %s, %s, %s)", (id_transaksi, id_user, no_hp, nama_provider, nominal_pulsa))
        cur.close()
        mysql.connection.commit()

        if(result):
            res_json = {
                'response_msg' : 'OK',
                'response_code' : 0
            }
        else:
            res_json = {
                'response_msg' : 'Transaksi pembelian pulsa tidak bisa ditambahkan.',
                'response_code' : -1414
            }

        return(res_json)

class products(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        str_sql_provider = ("SELECT * FROM provider")
        cur.execute(str_sql_provider)
        data_provider = cur.fetchall()

        str_sql_pulsa = ("SELECT * FROM pulsa")
        cur.execute(str_sql_pulsa)
        data_pulsa = cur.fetchall()
        cur.close()

        data_res = {
            'provider' : data_provider,
            'pulsa' : data_pulsa
        }

        keyss = list(data_res.keys())

        all_data = {'products':[]}
        for col in keyss:
            data = data_res[col]
            data_array = []
            for row in data:
                data_dict = {}
                attributes = list(row.keys())
                for attr in attributes:
                    # kalo datetime diconvert dlu jadi string
                    if(attr == 'waktu_transaksi'):
                        d = row[attr]
                        data_dict[attr] = d.strftime("%d %b, %Y")
                        # print(data_dict[attr])
                    # selain datetime
                    else: 
                        data_dict[attr] = row[attr]
                data_array.append(data_dict)
                product = {
                    col : data_array
                }
            all_data['products'].append(product)
        
        all_data['response_code'] = 0
        all_data['response_msg'] = 'OK'
        
        return all_data
        
class voices(Resource):
    def post(self):
        # check if the post has the file part
        if 'file' not in request.files:
            res_json = {
                'response_code' : -1411,
                'response_msg' : 'Request tidak mengandung file'
            }
            print(res_json)
            return res_json
        file = request.files['file']
        # if users does not select file browser also 
        # submit an empty part without filename
        if file.filename == '':
            res_json = {
                'response_code' : -1412,
                'response_msg' : 'File pada request kosong'
            }
            print(res_json)
            return res_json
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            attempt = request.form['name'] # ambil jumlah mencoba autentikasi 

            # ambil id_user atau id_transaksi didepannya
            id_file = filename.split('_')[0]
            # cek dulu prefix id_file
            if(id_file.startswith('USR')):
                # buat folder dengan di dalem folder users
                pathlib.Path(app.config['UPLOAD_FOLDER'], 'users', id_file).mkdir(exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'users', id_file, filename))
            else:
                # sebelum buat folder, cek dulu ada ga folder dengan nama id_transaksi di dalam folder transactions
                path_folder_transaksi = os.path.join(app.config['UPLOAD_FOLDER'], 'transactions', id_file)
                # print(attempt)
                # kalo udah ada
                if(os.path.isdir(path_folder_transaksi)):
                    # print('udah ada')
                    # buat lagi folder attempt di dalem id_transaksi
                    pathlib.Path(app.config['UPLOAD_FOLDER'], 'transactions', id_file, attempt).mkdir(exist_ok=True)
                    # save audio di /id_transaksi/attempt
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'transactions', id_file, attempt, filename))
                else: # kalo belom ada
                    # print('belom ada')
                    # buat folder transactions
                    pathlib.Path(app.config['UPLOAD_FOLDER'], 'transactions', id_file).mkdir(exist_ok=True)
                    # buat lagi folder attempt di dalem id_transaksi
                    pathlib.Path(app.config['UPLOAD_FOLDER'], 'transactions', id_file, attempt).mkdir(exist_ok=True)
                    # save audio di /id_transaksi/attempt
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'transactions', id_file, attempt, filename))
        
        res_json = {
            'response_code' : 0,
            'response_msg' : 'OK'
        }
        # print(res_json)
        return res_json

class authentication(Resource):
    def post(self):
        req_json = request.get_json()

        id_transaksi = req_json['id_transaksi']
        attempt = req_json['attempt']
        voices = req_json['voices']

        try:
            # dapatkan path folder id_transaksi dan folder attempt yang berisi audio yang telah diupload
            path_folder_transaksi = os.path.join(app.config['UPLOAD_FOLDER'], 'transactions', id_transaksi, attempt)

            # cek dulu apakah 5 rekaman sudah terupload ke dalam folder tsb
            count_file = len([name for name in os.listdir(path_folder_transaksi) if os.path.isfile(os.path.join(path_folder_transaksi, name))])
            if(count_file < 5):
                json_res = {
                    'response_code' : -1545,
                    'response_msg' : 'Gagal menggunduh rekaman transaksi'
                }
                print(json_res)
                return json_res
        except Exception as e:
            json_res = {
                'response_code' : -1545,
                'response_msg' : 'Gagal menggunduh rekaman transaksi'
            }
            return json_res
        
        #kalo udah 5 lanjutkan

        # sebelum insert ke db, features extraction dulu
        path_npz = features_extraction_with_mfcc_test(path_folder_transaksi, '/', id_transaksi)
        path_npz += '.npz'

        cur = mysql.connection.cursor()
        flag = 0

        id_user_1 = req_json['id_user']

        # select dulu path mfcc dari id_user
        sql_mfcc = ("SELECT path_mfcc FROM user WHERE id_user='"+ id_user_1 +"'")
        cur.execute(sql_mfcc)
        path_mfcc = cur.fetchall()[0]['path_mfcc']
        
        
        # prediksi model Speaker Verification
        y_pred_sv, dict_y_sv = predict_speaker_verification(model_sv, path_mfcc, path_folder_transaksi, path_npz)

        print("Hasil prediksi SV: ")
        print(dict_y_sv)


        if((y_pred_sv == 1).all()):
            print("SV berhasil, ")

            # prediksi model Speech Recognition
            y_pred_sr, y_truth, dict_y_sr = predict_speech_recognition(model_sr, path_folder_transaksi, path_npz)
            print("Hasil prediksi SR: ")
            print(dict_y_sr)

            if((y_pred_sr == y_truth).all()):
                print("SR berhasil")
                # update ke tabel transaksi bahwa transaksi berhasil
                cur.execute("UPDATE transaksi SET status_transaksi=%s WHERE id_transaksi = %s", (1, id_transaksi))
                mysql.connection.commit()

                # ambil nominal pulsa
                sql_nominal = cur.execute("SELECT nominal_pulsa FROM transaksi WHERE id_transaksi='"+ id_transaksi +"'")
                nominal = cur.fetchall()[0]['nominal_pulsa']

                print('Nominal: ' + str(nominal))

                # update saldo user
                cur.execute("UPDATE user SET saldo_user = saldo_user - %s WHERE id_user=%s", (nominal, id_user_1))
                mysql.connection.commit()

                json_res = {
                    'response_code' : 20, # benar
                    'response_msg' : 'Voice Authentication berhasil'
                }
            else:
                print("SV berhasil, SR gagal")
                cur.execute("UPDATE transaksi SET status_transaksi=%s WHERE id_transaksi = %s", (0, id_transaksi))
                mysql.connection.commit()

                json_res = {
                    'response_code' : -1510,
                    'response_msg' : 'Speaker Verification berhasil, Speech Recognition gagal'
                }
        else:
            print("SV gagal, SR gagal")

            # prediksi model Speech Recognition
            y_pred_sr , y_truth, dict_y_sr = predict_speech_recognition(model_sr, path_folder_transaksi, path_npz)
            print(y_pred_sr)

            cur.execute("UPDATE transaksi SET status_transaksi=%s WHERE id_transaksi = %s", (0, id_transaksi))
            mysql.connection.commit()

            json_res = {
                'response_code' : -1511,
                'response_msg' : 'Speaker Verification gagal'
            }

        # insert prediksi ke db
        for voice in voices:
            nama_rekaman = voice['nama_rekaman']
            id_user = voice['id_user']
            id_user_1 = id_user
            kode_angka = voice['kode_angka']

            # path_rekaman_transaksi = os.path.join(path_folder_transaksi, nama_rekaman)
            path_rekaman_transaksi = path_folder_transaksi

            y_pred_sv_i = str(dict_y_sv[int(kode_angka)])
            y_pred_sr_i = str(dict_y_sr[int(kode_angka)])

            # print()
            # print("INSERT INTO rekaman_transaksi (attempt, nama_rekaman_transaksi, id_transaksi, kode_angka, id_user, path_rekaman, y_pred_sv, y_pred_sr) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (attempt, nama_rekaman, id_transaksi, kode_angka,  y_pred_sr_i, y_pred_sv_i, id_user, path_rekaman_transaksi))

            result = cur.execute("INSERT INTO rekaman_transaksi (attempt, nama_rekaman_transaksi, id_transaksi, kode_angka, id_user, path_rekaman, y_pred_sv, y_pred_sr) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (attempt, nama_rekaman, id_transaksi, kode_angka, id_user, path_rekaman_transaksi, y_pred_sv_i, y_pred_sr_i))
            if(result):
                mysql.connection.commit()
        cur.close()
        return json_res
        
        
# Tambahin resource ke dalam api
api.add_resource(session, '/api/session') # buat login

api.add_resource(users, '/api/users', '/api/users/<id_user>') # buat dapetin 1 data user dan mendaftarkan user baru, delete akun kalo keluar aplikasi sebelum selesai daftar suara
api.add_resource(user_profile, '/api/users/<id_user>/profile', endpoint='profile') # buat update 1 data user
api.add_resource(user_password, '/api/users/<id_user>/password', endpoint='password') # buat update 1 password user
api.add_resource(user_active, '/api/users/<id_user>/active', endpoint='active') # buat aktifin akun setelah melakukan pendaftaran suara

api.add_resource(transactions, '/api/transactions/<id_user>','/api/transactions') # resource untuk dapetin seluruh transaksi, dan utk pembelian pulsa

api.add_resource(products, '/api/products') # resource untuk dapetin pulsa dan provider

api.add_resource(voices, '/api/voices') # resource untuk upload audio file

api.add_resource(authentication, '/api/authentication') # resource untuk prediksi rekaman user melalui proses voice authentication
# ------------------------------------------------------------------------

class SpeakerVerificationModel:
    """docstring for ClassName"""
    def __init__(self):
        self.model = load_model("./models/SV/model_weights_1_1.h5")
        # self.model._make_predict_function()
        self.graph = tf.compat.v1.get_default_graph()

    # def predict(self, X=[]):
    #     return self.model.predict(X)

class SpeechRecognitionModel:
    """docstring for ClassName"""
    def __init__(self):
        self.model = load_model("./models/SR/model_weights_SR_3_2.h5")
        # self.model._make_predict_function()
        self.graph = tf.compat.v1.get_default_graph()

    # def predict(self, X):
    #     return self.model.predict(X)

def load_keras_model():
    global model_sv, model_sr 
    print(" * Keras model loading..")
    model_sv = SpeakerVerificationModel()
    # model_sv.model.summary()
    model_sr = SpeechRecognitionModel()
    # model_sr.model.summary()
    print(" * Keras model loaded.")

# main program
load_keras_model()

try:
    if mysql is None:
        print("database object is empty.")
except NameError:
    print("cannot connect to database.")
print(" * Starting flask web server...")

if __name__ == '__main__':  
    app.run(debug=True, host='0.0.0.0', threaded=False)



