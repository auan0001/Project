#!/bin/python
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
while True:
    ser.write(bytes(b'R'))
    line = ser.readline().decode()
    print(line)
    time.sleep(0.5)
