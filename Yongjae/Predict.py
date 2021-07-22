import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
import serial

model = tf.keras.models.load_model('Sensor2thetaMean11.h5')
scaler = load('scaler_01.pkl')

simple = serial.Serial('COM4',115200,timeout=1)

tof = [0,0,0,0,0,0,0,0,0,0]

toRad = float(np.pi/180)

while (True):
    while (simple.inWaiting()==0):
        pass
    SdataPacket = simple.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")
    if len(SsplitPacket) >= 10:
        for i in range(0,10):
            tof[i] = float(SsplitPacket[i])
            #print(tof[i],end=' ')

        tof2 = np.array(tof).reshape(-1,1).T
        tof3 = scaler.transform(tof2)
        #print(tof.shape)
        Predict = model.predict(tof3)
        print('theta: ', Predict[:,0])




