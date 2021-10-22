import serial, time, csv
import numpy as np

tof = np.zeros(24)
arduino = serial.Serial('COM3',115200,timeout=1)

while True:
    while (arduino.inWaiting()==0):
        pass
    SdataPacket = arduino.readline()
    SdataPacket = str(SdataPacket, "utf-8")
    SsplitPacket = SdataPacket.split(" ")

    file_path = "C:/Users/Lab/Desktop/LYS/Software/LABS_2.0.csv"
    if len(SsplitPacket) >= len(tof):
        file = open(file_path, 'a',encoding = "utf-8", newline='')
        csv_writer = csv.writer(file)
        csv_writer.writerow(SsplitPacket)
        for i in range(0,24):
            tof[i] = float(SsplitPacket[i])
            print(tof[i],end=' ')
    print("")