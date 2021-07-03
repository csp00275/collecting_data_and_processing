from vpython import *
from time import *
import numpy as np
import math


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


R = 80  #cylinder D=160
L = 216 #cylinder

sensor_cylinder = cylinder(axis=vector(0,0,1),pos=vector(0,0,0),radius=R,length=L,opacity=.3)

frontArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.purple, axis=vector(1,0,0))
upArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.magenta, axis=vector(0,1,0))
sideArrow = arrow(length=AxisLen,shaftwidth=AxisWid,color=color.orange, axis=vector(0,0,1))

while (True):
    pitch = 0 * toRad
    for yaw in np.range(0,2 * np.pi,.01)
        rate(50)
        k = vector(cos(yaw)*cos(pitch), sin(pitch), sin(yaw) * cos(pitch))

        y = vector(0,1,0)
        s = cross(k,y)
        v = cross(s,k)

        frontArrow.axis = k
        sideArrow.axis = s
        sideArrow.length = 2
        upArrow.length = 4
        upArrow.axis = v

