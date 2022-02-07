#!/bin/python
import serial

ser = serial.Serial("/dev/ttyUSB0", 9600)


while True:
    ser.write(41)
    line = ser.readline().decode()
    print(line)
