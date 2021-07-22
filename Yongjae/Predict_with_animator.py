import tensorflow as tf
import numpy as np
import serial
from joblib import dump, load
from vpython import *
from time import *

simple = serial.Serial('COM4',115200,timeout=1)

tof = [0,0,0,0,0,0,0,0,0,0]
DisSenTheta=[0,0,0,0,0,0,0,0,0,0,0,0]
ball=[0,0,0,0,0,0,0,0,0,0,0,0]

toRad = 2*np.pi/360
toDeg = 1/toRad

#canvas
scene.range = 200
scene.forward = vector(-1,-1,-1)
scene.width = 480
scene.height = 640
scene.background = color.white
scene.up = vector(0,0,1)


# xzy axis
axis_length = 40
axis_width = 4
xarrow = arrow(length=axis_length,shaftwidth=axis_width,color=color.red, axis=vector(1,0,0))
zarrow = arrow(length=axis_length,shaftwidth=axis_width,color=color.green, axis=vector(0,0,1))
yarrow = arrow(length=axis_length,shaftwidth=axis_width,color=color.blue, axis=vector(0,1,0))

D = 160 #cylinder
R = D/2
L = 216 #cylinder

sensor_cylinder = cylinder(axis=vector(0,0,1),pos=vector(0,0,0),radius=R,length=L,opacity=.3)

#센서
DisSenLen = 15
DisSenWid = 10
DisSenHeight = 2 # thickness

for i in range(0,10):
    DisSenR = 50
    DisSenTheta[i] = 36 * i
    DisSenX = DisSenR*cos(DisSenTheta[i]*toRad)
    DisSenY = DisSenR*sin(DisSenTheta[i]*toRad)
    DisSenZ = 105

    ballR = 30 + DisSenR
    ballX = ballR * cos(DisSenTheta[i] * toRad)
    ballY = ballR * sin(DisSenTheta[i] * toRad)
    ballz = DisSenZ

    DisSen = box(size = vector(DisSenLen,DisSenHeight,DisSenWid), pos = vector(DisSenX,DisSenY,DisSenZ),up = vector(DisSenX,DisSenY,0),color = vector(.62,0,.63))
    ball[i] = sphere(radius=2, pos=vector(ballX, ballY, DisSenZ), color=vector(1, 0, 0))




conArrowXDir=0
conArrowYDir=0
conArrowXPos=0
conArrowYPos=0
conArrowLen=80


ConArrow0 = arrow(length=conArrowLen, shaftwidth=5, color=color.yellow)

model = tf.keras.models.load_model('Mean11_0722.h5')
scaler = load('scaler_01.pkl')



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
            ball[i].pos.x= (tof[i]+DisSenR)*cos(DisSenTheta[i]*toRad)
            ball[i].pos.y= (tof[i]+DisSenR)*sin(DisSenTheta[i]*toRad)
            print(tof[i],end=' ')

        tof2 = np.array(tof).reshape(-1,1).T
        tof3 = scaler.transform(tof2)
        #print(tof.shape)
        Predict = model.predict(tof3)

        r = R - 10
        theta0 = Predict[:,0]
        z = 110

        costheta = cos(toRad * theta0)
        sintheta = sin(toRad * theta0)

        conArrowXDir = r * costheta
        conArrowYDir = r * sintheta

        conArrowLen = 80

        conArrowXPos = (R + conArrowLen) * costheta
        conArrowYPos = (R + conArrowLen) * sintheta
        ConArrow0.axis = vector(-conArrowXDir, -conArrowYDir, 0)
        ConArrow0.pos = vector(conArrowXPos, conArrowYPos, z)

        print("theta0=", theta0, "z=", z)

    rate(50)

