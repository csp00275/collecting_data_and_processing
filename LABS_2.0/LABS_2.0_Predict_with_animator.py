from vpython import *
import serial, time , math, csv
from time import *
import numpy as np
import tensorflow as tf
from joblib import dump, load

# Import model and scaler
model = tf.keras.models.load_model("C:/Users/Lab/Desktop/LYS/Software/LABS_2.0/myModel/2021_09_28_70ms_3ea_Data_3z.h5")
scaler = load('C:/Users/Lab/Desktop/LYS/Software/LABS_2.0/myScaler/2021_09_28_70ms_3ea_Data_3z_SS.pkl')

# 24 sensors
SenNum = 24
DisSenTheta=np.zeros(SenNum)
tof = np.zeros(SenNum)
ball = [0*i for i in range(0,SenNum)]

# Math
toRad = 2*np.pi/360
toDeg = 1/toRad

# Serial
arduino = serial.Serial('COM3',115200,timeout=1)  # COM8 Arduino NanoEvery
                                                  # COM3 Arduino Mega 2560

# Canvas
scene.range = 200
scene.forward = vector(-1,-1,-1)
scene.width = 480
scene.height = 640
scene.background = color.white
scene.up = vector(0,0,1)

# xyz axis
AxisLen = 40
AxisWid = 4
xArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.red, axis=vector(1,0,0))
yArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.blue, axis=vector(0,1,0))
zArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.green, axis=vector(0,0,1))

R = 105  #cylinder D=210
L = 160 #cylinder

sensor_cylinder = cylinder(axis=vector(0,0,1),pos=vector(0,0,0),radius=R,length=L,opacity=.3)

# Sensor PCB generation
DisSenLen = 10.7
DisSenWid = 13.4
DisSenHeight = 1.7 # thickness


for i in range(0,24):
    eight = divmod(i, 8) # eight[0] 몫   eight[1] 나머지
    four = divmod(i, 4) # four[0] 몫   four[1] 나머지
    ind = divmod(four[0],2) # indicator[0] 몫 indicator[1] 나머지  (ind : indicator)

    DisSenR = 50 #센서 반지름
    DisSenTheta[i] = ((-1) ** ind[1]) * 30 * eight[1] + 210 * ind[1] + 120 * ind[0]
    # print('i:',i, ' four[0]:',four[0],' four[1]:',four[1],' ind[0]:',ind[0],' ind[1]:',ind[1],' theta:',DisSenTheta[i])
    DisSenX = DisSenR*cos(DisSenTheta[i]*toRad)
    DisSenY = DisSenR*sin(DisSenTheta[i]*toRad)
    DisSenZ = 52 + ind[1] * 42

    ballR = 30+DisSenR
    ballX = ballR*cos(DisSenTheta[i]*toRad)
    ballY = ballR*sin(DisSenTheta[i]*toRad) #센서랑 같은 위치 반지름만 30+
    ballZ = DisSenZ

    DisSen = box(size=vector(DisSenLen, DisSenHeight, DisSenWid), pos=vector(DisSenX, DisSenY, DisSenZ),
                 up=vector(DisSenX, DisSenY, 0), color=vector(.62, 0, .63))
    ball[i] = sphere(radius = 2,pos = vector(ballX,ballY,ballZ),color= vector(1,0,0))

    # Contact Arrow
    conArrowXDir = 0
    conArrowYDir = 0
    conArrowXPos = 0
    conArrowYPos = 0
    conArrowLen = 80

    ConArrow0 = arrow(length=conArrowLen, shaftwidth=5, color=color.yellow)

while True:

    while (arduino.inWaiting()==0):
        pass
    SdataPacket = arduino.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")

    if len(SsplitPacket) >= SenNum:
        for i in range(0,SenNum):
            tof[i] = float(SsplitPacket[i])
            ball[i].pos.x= (tof[i]+DisSenR)*cos(DisSenTheta[i]*toRad)
            ball[i].pos.y= (tof[i]+DisSenR)*sin(DisSenTheta[i]*toRad)
            print(tof[i],end=' ')

        tof2 = np.array(tof).reshape(-1, 1).T
        tof3 = scaler.transform(tof2)
        # qqqrint(tof.shape)
        Predict = model.predict(tof3)

        r = R - 10
        # theta0 = np.arctan2(Predict[:,1],Predict[:,0])*toDeg
        z = Predict[:, 0] * 50 + 50 + 30

        costheta = Predict[:, 2]
        sintheta = Predict[:, 1]

        conArrowXDir = r * costheta
        conArrowYDir = r * sintheta

        conArrowLen = 80

        conArrowXPos = (R + conArrowLen) * costheta
        conArrowYPos = (R + conArrowLen) * sintheta
        ConArrow0.axis = vector(-conArrowXDir, -conArrowYDir, 0)
        ConArrow0.pos = vector(conArrowXPos, conArrowYPos, z)

    print("")

    rate(100)
