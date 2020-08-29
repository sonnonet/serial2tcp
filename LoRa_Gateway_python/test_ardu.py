import serial

ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
)

while True:
    if ser.readable():
        res = ser.readline()
        print res

