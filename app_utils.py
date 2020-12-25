import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf

import librosa 
from librosa.feature import mfcc

import glob
import os
import soundfile as sf
import itertools

from tempfile import TemporaryFile
from pathlib import Path

# Lib keras
from keras.utils import to_categorical
from keras.models import load_model
from keras.models import model_from_json
from keras.models import Model, Sequential
from keras.layers import Dense, Input, Dropout, LSTM, Activation

# Lib scikit learn
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

maxi_duration = 2.89 # nnti diganti
# max_signal = 127600 # nnti diganti
max_signal = 63800

# load model Speech Recognition
# model_sr = load_model("./models/SR/model_and_weights_8_1.h5")
# model_sv = load_model("./models/SV/model_weights_1.h5")
# graph = tf.get_default_graph()

# Fungsi untuk melakukan ekstraksi fitur menggunakan MFCC untuk file pendaftaran suara
def features_extraction_with_mfcc_test(path, split_path_separator, id_user_daftar):
    print('FEATURES EXTRACTION WITH MFCC ---------------------')
    dir_suara = path
    len_dir_suara = len([name for name in os.listdir(dir_suara) if os.path.isfile(os.path.join(dir_suara, name))])

    #menghitung total file
    data_length = len_dir_suara

    print('The path of dataset: ' + dir_suara)
    print('The total file inside dataset: ' + str(len_dir_suara))

    global max_signal
    global maxi_duration
    max_sig = max_signal
    max_duration = maxi_duration

    #definisikan beberapa variabel
    sampling_rate = 22050
    
    # membuat array untuk menampung seluruh file audio
    test = np.zeros((data_length, max_signal + 1))

    i = 0

    file_name = []

    dict_angka = {
        '1' : 1,
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9
    }

    # cek apakah udah pernah features extraction id transaksi apa blm
    my_file = Path(path + '/' + id_user_daftar + '.npz')
    if my_file.is_file():
    	# file exists
    	npz_file_name = os.path.join(dir_suara, id_user_daftar)
    	print(str(my_file) + ' already exists ----------------------')
        
    	return npz_file_name
    else: # file not exists
	    for path in glob.glob(dir_suara + '\\*.wav'):
	        file_name_path = path.split(split_path_separator) # mendapatkan nama file dari string path
	        str_file_name = file_name_path[-1] # ambil elemen paling terakhir
	        file_name.append(str_file_name) # memasukan setiap nama file ke dalam list
	        arr_file_name = str_file_name.split("_") # split string by _ 
	        digit_angka = arr_file_name[-1][:1] # ambil digit angka diucapkan dalam rekaman (cth: satu)

	        # print(arr_file_name)
	        # print()
	        # print(digit_angka)
	        
	        # signal, sample_rate = librosa.load(path, sr=sampling_rate) #membaca file audio pada path 
	        # duration = librosa.get_duration(y=signal, sr=sampling_rate) 

	        # pake soundfile
	        data, samplerate = sf.read(path, dtype='float32')
	        data = data.T
	        signal = librosa.resample(data, samplerate, samplerate)
	        
	        # padding signal yang lebih dari max_sig
	        if(signal.shape[0] < max_sig):
	            perbedaan = max_sig - signal.shape[0]
	            padding = np.zeros((1,perbedaan))
	            test[i, 0:max_sig] = np.concatenate((signal, padding), axis=None)
	        elif(signal.shape[0] > max_sig):
	            test[i, 0:max_sig] = signal[0:max_sig]
	        else:
	            test[i, 0:max_sig] = signal
	            
	        test[i, -1] = dict_angka[digit_angka]
	        i += 1

	    print('Test contains audio vector shape: ' + str(test.shape))
	    
	    X_test = test[:, 0:max_sig] 
	    Y_test = test[:, -1]

	    m = X_test.shape[0] #total audio file
	    n = X_test.shape[1] #the length of 1 audio file

	    print("X test shape: " + str(X_test.shape))
	    print("Y test shape: " + str(Y_test.shape))

	    num_ceps = 13
	    num_mels_filter = 40

	    hop_length=512      #(number of samples between frames)
	    n_fft=2048          #(number of samples per frame in STFT-like analyses)
	    #output frame length = (seconds) * (sample rate) / (hop_length)
	    num_frames = round(round(max_duration, 1) * sampling_rate / hop_length) 

	    mfcc_vec = np.zeros((m, num_frames, num_ceps))

	    print("Number of cepstral coefficient: " + str(num_ceps))
	    print("Number of mel filterbank: " + str(num_mels_filter))
	    print("Number of samples between frames: " + str(hop_length))
	    print("Number of samples per frame using STFT: " + str(n_fft))
	    print("Number of frames used: " + str(num_frames) )
	    print()
	    print("MFCC features vector shape: " + str(mfcc_vec.shape))

	    # untuk setiap audio file ke-i
	    for i in range(0, m):
	        mfcc_return = mfcc(y=X_test[i,:], n_mfcc=num_ceps, hop_length=hop_length, n_mels=num_mels_filter).T
	        # untuk setiap frame ke-k pada audio file ke-i
	        for k in range(0, num_frames):
	            mfcc_vec[i, k, 0:num_ceps] = mfcc_return[k,:]

	    X = mfcc_vec
	    Y = Y_test.reshape(m,1)

	    print("Data X shape: " + str(X.shape))
	    print("Data Y shape: " + str(Y.shape))

	    npz_file_name = os.path.join(dir_suara, id_user_daftar)
	    np.savez(npz_file_name, x=X, y=Y, file_name=file_name)

	    print('Successfully build ' + npz_file_name + ' npz file')
	    print('-----------------------------------------------')

	    return npz_file_name

def predict_speech_recognition(model_sr, base_path, path_mfcc_file, file_csv='hasil_prediksi_sr.csv'):
    print("PREDICT SPEECH RECOGNITION---------------")
    mfcc_npz = np.load(path_mfcc_file)

    X_test = mfcc_npz['x']
    Y_test = mfcc_npz['y']   
    test_file_name = mfcc_npz['file_name']

    data_len = X_test.shape[0]
    feat_dim = X_test.shape[2]
    time_step = X_test.shape[1]
    num_classes = 9 #1, 2, 3, ..., 9

    print("Data X shape: " + str(X_test.shape))
    print("Data Y shape: " + str(Y_test.shape))
    print("Data File name shape: " + str(test_file_name.shape))

    # to categorical
    Y_test_cat = to_categorical((Y_test-1).T, num_classes=9)
    Y_test_cat = Y_test_cat[0]

    print("Y test one hot encoding shape: " + str(Y_test_cat.shape))

    # prediksi data testing
    # global graph
    # with graph.as_default():
    with model_sr.graph.as_default():
        Y_pred_test = model_sr.model.predict(X_test)

    Y_pred_test_cat = np.argmax(Y_pred_test, axis=1, out=None) + 1

    score_test = f1_score(Y_test, Y_pred_test_cat, average='micro')
    test_acc= accuracy_score(Y_test, Y_pred_test_cat)

    print("LSTM F1 Score on test data: " + str(score_test))
    print('LSTM Accuracy on test data: ' + str(test_acc))

    # Compute confusion matrix
    # cnf_matrix = confusion_matrix(Y_test, Y_pred_test_cat)
    # np.set_printoptions(precision=2)

    # print(cnf_matrix)

    data_list = {
        'file_name' : test_file_name,
        'Y_test_prob_1' : Y_pred_test[:, 0],
        'Y_test_prob_2' : Y_pred_test[:, 1],
        'Y_test_prob_3' : Y_pred_test[:, 2],
        'Y_test_prob_4' : Y_pred_test[:, 3],
        'Y_test_prob_5' : Y_pred_test[:, 4],
        'Y_test_prob_6' : Y_pred_test[:, 5],
        'Y_test_prob_7' : Y_pred_test[:, 6],
        'Y_test_prob_8' : Y_pred_test[:, 7],
        'Y_test_prob_9' : Y_pred_test[:, 8],
        'Y_test' : Y_test.reshape(data_len),
        'Y_pred_test' : Y_pred_test_cat
    }
    df_testing = pd.DataFrame(data_list)
    df_testing.to_csv(base_path + '\\' + file_csv, index=False)

    print('Successflly build ' + str(file_csv) + ' csv file')

    Y_truth_test = Y_test.ravel()

    dict_y = dict(zip(tuple(Y_test.ravel().astype(int)), tuple(Y_pred_test_cat.ravel())))

    return Y_pred_test_cat, Y_truth_test, dict_y

def predict_speaker_verification(model_sv, path_mfcc_user, base_path, path_mfcc_file, file_csv='hasil_prediksi_sv.csv'):
    print("PREDICT SPEAKER VERIFICATION---------------")
    mfcc_npz = np.load(path_mfcc_file) # load mfcc transaksi
    user_npz = np.load(path_mfcc_user) # load mfcc user

    # ambil kode angka dari mfcc transaksi
    Y_test = mfcc_npz['y'].ravel() # jadiin 1 dimensi
    X_test = mfcc_npz['x']
    test_file_name = mfcc_npz['file_name']

    # ambil MFCC user 
    mfcc_user = user_npz['x'] # jadiin 1 dimensi
    file_name = user_npz['file_name']

    print("Y test shape: " + str(Y_test.shape))
    print("X test shape: " + str(X_test.shape))
    print("File name test shape: " + str(test_file_name.shape))
    print("MFCC user shape: " + str(mfcc_user.shape))
    print("Filename user shape: " + str(file_name.shape))

    user_feat = np.zeros((5, mfcc_user.shape[1], mfcc_user.shape[2]))

    idx = 0
    for i in Y_test.astype(int): # ubah float menjadi integer
        print(i)
        user_feat[idx, :, :] = mfcc_user[i-1, :, :] # i - 1 karena index array mulai dari 0
        idx += 1

    X_left_test = np.copy(X_test)
    X_right_test = np.copy(user_feat)

    print("X left test shape (from transactions) : " + str(X_left_test.shape))
    print("X right test shape (from user) : " + str(X_right_test.shape))

    # global graph
    # with graph.as_default():
    # tess = [X_left_test, X_right_test]
    with model_sv.graph.as_default():
        Y_pred_test = model_sv.model.predict([X_left_test, X_right_test])

    Y_pred_test_prob = np.copy(Y_pred_test)

    Y_pred_test[Y_pred_test <= 0.5] = 0
    Y_pred_test[Y_pred_test > 0.5] = 1

    # print("Y test: " + str(Y_pred_test.shape))
    # print(Y_pred_test)
    # print("Y test prob: " + str(Y_pred_test_prob.shape))
    # print(Y_pred_test_prob)

    s = np.subtract(Y_test.astype(int), 1) # kurangin dulu 1 karena array buat nyimpen file name mulai dari 0

    data_list = {
        'Y_test' : Y_test.ravel(),
        'File name' : np.take(file_name, s),
        'Y_pred_test' : Y_pred_test.ravel(),
        'Y_pred_test_prob' : Y_pred_test_prob.ravel()
    }

    df_testing = pd.DataFrame(data_list)

    df_testing.to_csv(base_path + '\\' + file_csv, index=False)
    print('Successflly build ' + str(file_csv) + ' csv file')

    dict_y = dict(zip(tuple(Y_test.ravel().astype(int)), tuple(Y_pred_test.ravel())))

    return Y_pred_test.ravel().astype(int), dict_y

    # return Y_pred_test.ravel().astype(int)


# base_path = "C:\\web_flask\\voices\\transactions\\TRS898983\\1"
# path_file = "C:\\web_flask\\voices\\transactions\\TRS898983\\1\\TRS898983.npz"
# predict_speech_recognition(base_path, path_file)
