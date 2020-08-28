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
        
        tempRegV =  regV[0:regV.find('.')]
        tempInitV =  initV[0:initV.find('.')]
        tempMaxV =  maxV[0:maxV.find('.')]

#        print "RegValue : " + tempRegV + " InitValue : " + tempInitV + " MaxValue : " + tempMaxV

        if(tempRegV == 'O'):
            intRegV = 0
        else:
            intRegV = int(tempRegV)
        

        intInitV = int(tempInitV)
        intMaxV = int(tempMaxV)
        
#        print intInitV
#        print intMaxV
        
        #result = intRegV + intInitV + intMaxV
        #print result
        
#        arrayTest = [0,intInitV,intMaxV]

        kmote.write(bytes(bytearray([intRegV])))
        kmote.write(bytes(bytearray([intInitV])))
        kmote.write(bytes(bytearray([intMaxV])))
        
#        kmote.write(1 + intInitV + intMaxV)


     
    except Exception as e:
        print("Exception read") + str(e)
    
    time.sleep(1)
