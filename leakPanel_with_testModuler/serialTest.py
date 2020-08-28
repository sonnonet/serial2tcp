import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
kmote = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)


while(True):
    try:
        rcvBuf = bytearray()
        ser.reset_input_buffer()
        rcvBuf = ser.read_until(size=40)
#        print rcvBuf.find('G')
        regV = rcvBuf[rcvBuf.find('G')+2:rcvBuf.find('I')-1]
        initV = rcvBuf[rcvBuf.find('T')+2:rcvBuf.find('M')-1]
        maxV = rcvBuf[rcvBuf.find('X')+2:len(rcvBuf)-1]

        print "RegStr : " + regV + " InitStr : " + initV + " MaxStr : " + maxV
        
        intRegV =  regV[0:regV.find('.')]
        intInitV =  initV[0:initV.find('.')]
        intMaxV =  maxV[0:maxV.find('.')]

        print "RegValue : " + intRegV + " InitValue : " + intInitV + " MaxValue : " + intMaxV
        
        #result = intRegV + intInitV + intMaxV
        #print result
        
        kmote.write(intRegV)
#        kmote.write(int(intInitV))
        
#        kmote.write(1 + intInitV + intMaxV)


     
    except Exception as e:
        print("Exception read") + str(e)
    
    time.sleep(1)
