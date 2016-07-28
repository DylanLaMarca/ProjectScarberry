import serial
import time

ser = serial.Serial('COM6',9600)
time.sleep(5)
print('Write: 30')
ser.write('5')
print('Wrote: 30')
time.sleep(5)
print('Write: .5')
ser.write('.2/')
print('Wrote: .5')
while True:
    print ser.read()
    print('.')