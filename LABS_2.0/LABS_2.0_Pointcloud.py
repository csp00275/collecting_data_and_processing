import serial, time, csv
from vpython import *
import numpy as np

run_date = time.strftime("%Y_%m_%d")
run_time = time.strftime("run_%H_%M_%S")

num = 24

tof = np.zeros(num)
arduino = serial.Serial('COM3',115200,timeout=1)  # COM8 arduino nanoevery

# print("Starting Conversation with Arduino")
#
#
# SayingTo = input()
#
# SayingToArduino = SayingTo.encode("utf-8")
# arduino.write(SayingToArduino)
# print(SayingToArduino)
# time.sleep(1)


DisSenTheta=np.zeros(num)
ball = [0*i for i in range(0,24)]
print(len(ball))

#Math
toRad = 2*np.pi/360
toDeg = 1/toRad

#canvas
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

#센서
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




while True:

    while (arduino.inWaiting()==0):
        pass
    SdataPacket = arduino.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")

    file_path = "C:/Users/Lab/Desktop/LYS/Coding/Python/"+run_date+"_70ms_3ea_pointcloud_"+run_time+".csv"
    if len(SsplitPacket) >= len(tof):
        file = open(file_path, 'a',encoding = "utf-8", newline='')
        csv_writer = csv.writer(file)
        csv_writer.writerow(SsplitPacket)
        for i in range(0,24):
            tof[i] = float(SsplitPacket[i])
            print(tof[i],end=' ')
        for i in range(0,24):
            tof[i] = float(SsplitPacket[i])
            ball[i].pos.x= (tof[i]+DisSenR)*cos(DisSenTheta[i]*toRad)
            ball[i].pos.y= (tof[i]+DisSenR)*sin(DisSenTheta[i]*toRad)
    print("")
    rate(100)
