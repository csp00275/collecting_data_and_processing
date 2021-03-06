import numpy as np
import tensorflow as tf
from joblib import dump, load
import serial
import time

model = tf.keras.models.load_model('210805_70ms_Mean3ea_wo06.h5')
scaler = load('210805_70ms_Mean3_SS.pkl')

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
        Predict_prev = time.time()
        Predict = model.predict(tof3)
        print('Predict Time :', time.time() - Predict_prev,'cos: ', Predict[:,0],'sin: ', Predict[:, 1])




