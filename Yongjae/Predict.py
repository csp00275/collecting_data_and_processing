import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import serial

model = tf.keras.models.load_model('E100_h128_NoR.h5')

simple = serial.Serial('COM4',115200,timeout=1)

tof = [0,0,0,0,0,0,0,0,0,0]

while (True):
    while (simple.inWaiting()==0):
        pass
    SdataPacket = simple.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")
    if len(SsplitPacket) >= 10:
        for i in range(0,10):
            tof[i] = float(SsplitPacket[i])
            print(tof[i],end=' ')

        tof2 = np.array(tof).reshape(-1,1).T
        # print(tof.shape)
        Predict = model.predict(tof2)
        print('theta: ', Predict[:,0], 'z: ',Predict[:,1])




