#!/bin/python
import serial

ser = serial.Serial("/dev/ttyUSB0", 9600)

while True:
    line = ser.readline().decode()
    print(line)
