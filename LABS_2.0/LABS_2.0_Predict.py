import numpy as np
import tensorflow as tf
from joblib import dump, load
import serial
import time

# import model and scaler
model = tf.keras.models.load_model('LABS_v2/210903_70ms_3ea_epoch250_wor4.h5')
scaler = load('LABS_v2/210903_70ms_Mean3_SS.pkl')

simple = serial.Serial('COM3',115200,timeout=1)

SenNum = 24
tof = np.zeros(SenNum)

# mat
toRad = float(np.pi/180)
toDeg = float(1/toRad)

while (True):
    while (simple.inWaiting()==0):
        pass
    SdataPacket = simple.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")
    if len(SsplitPacket) >= 24:
        for i in range(0,SenNum):
            tof[i] = float(SsplitPacket[i])
            #print(tof[i],end=' ')

        tof2 = np.array(tof).reshape(-1,1).T
        tof3 = scaler.transform(tof2)
        #print(tof.shape)
        Predict_prev = time.time()
        Predict = model.predict(tof3)
        Theta = np.arctan2(Predict[:,2],Predict[:,1])*toDeg
        z = Predict[:,0]*50+50+30
        print('Predict Time :', time.time() - Predict_prev,'z: ', z,'cos: ', Predict[:,1],'sin: ',
              Predict[:,2],'Theta: ',Theta)





