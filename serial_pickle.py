import serial 
import pickle
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical


serial_output = "2.090534e+02, -7.320956e+00, -6.026335e+00, -7.514086e-01, 1.762598e+00, -1.768363e+00, 1.398138e+00, 3.181960e-01, -4.378806e-02, -9.600201e-01, -1.858483e-02, 1.457793e-01, -5.042020e-01, -3.429266e-01, 4.438075e-01, 9.787656e-02, -4.047304e-01, 5.904381e-01, 9.183031e-01, 9.094788e-01, -3.539270e-01, -4.380997e-01, -3.737924e-01, 4.209963e-01, 4.257320e-01, 9.710624e-01, 6.781266e-01, -5.371231e-01, -9.378346e-01, 1.240507e-01, 5.653303e-01, 9.201310e-01, 5.733954e-01, -1.196257e-01, -5.663368e-02, 1.228863e-01, -3.110337e-01, -3.143343e-01, 1.872355e-01, -3.367165e-01, 4.191162e-14"

def parse_line(in_line):
	# array of strings split on delimiter
	# convert to an array of floats 
	data = in_line.split(", ")
	data = np.array(data)
	#print(data)
	data = data.astype(np.float)
	data = data[1:]
	#print(data)
	return data

parse_line(serial_output)

'''
device_name = '/dev/tty.usbmodem1441202'

ser = serial.Serial(device_name)

ser.baudrate = 115200

ser.open()

data = np.array()

# '-' will separate lines
take data and put into arrays of arrays (2D array)
run that through the model imported as pickle

# data comes one as a line
while(ser.is_open()):
	byte = read
'''

arr = []

with open('car_horn.txt', 'r') as fp:
	line = fp.readline()
	while(len(line) > 0):
		arr.append(parse_line(line))
		line = fp.readline()

arr = np.array(arr)
print(arr)

# transpose it
arr = arr.T

max_pad_len = 174
pad_width = max_pad_len - arr.shape[1]

arr = np.pad(arr,pad_width=((0,0),(0,pad_width)), mode='constant')

# unpickling the pickles
loaded_model = pickle.load(open('CNN_model.pickle', 'rb'))
le = pickle.load(open('LE.pickle', 'rb'))

num_rows = 40
num_columns = 174
num_channels = 1

print(arr.shape)

def print_prediction(prediction_feature):
    #prediction_feature = extract_features(file_name) 
    #print(prediction_feature)
    prediction_feature = prediction_feature.reshape(1, num_rows, num_columns, num_channels)
    #print(prediction_feature)
    predicted_vector = loaded_model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector) 
    print("The predicted class is:", predicted_class[0], '\n') 
    
    predicted_proba_vector = loaded_model.predict_proba(prediction_feature) 
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)): 
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )


print_prediction(arr)
