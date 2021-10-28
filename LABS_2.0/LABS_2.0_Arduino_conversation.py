import serial, time, csv
import numpy as np

sennum=28
tof = np.zeros(sennum)
arduino = serial.Serial('COM3',115200,timeout=1)
run_date = time.strftime("%Y_%m_%d")
run_time = time.strftime("run_%H_%M_%S")

print("Starting Conversation with Arduino")
print(len(tof))
SayingTo = input()

SayingToArduino = SayingTo.encode("utf-8")
arduino.write(SayingToArduino)
print(SayingToArduino)
time.sleep(1)

while True:

    while (arduino.inWaiting()==0):
        pass
    SdataPacket = arduino.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")

    file_path = "C:/Users/Lab/Desktop/LYS/Software/LABS_3.0/myData/"+run_date+"_70ms_3ea_Data_"+run_time+"_from140.csv"


    if len(SsplitPacket) == len(tof)+1:
        file = open(file_path, 'a',encoding = "utf-8", newline='')
        csv_writer = csv.writer(file)
        csv_writer.writerow(SsplitPacket)
        for i in range(0,sennum):
            tof[i] = float(SsplitPacket[i])
            print(tof[i],end=' ')
    print("")