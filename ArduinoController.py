import serial
import time

ser = serial.Serial('COM6',9600)
while True:
     print ser.readline()