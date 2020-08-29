import serial
import time
from datetime import datetime
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
#ser.close()
#ser.open()
 
#ser.write("testing")
counter=0
try:
    while 1:
#        ser.write("AT+SEND 2:KX15JTQP000020082\n")
#        time.sleep(1)
#        ser.write("AT+SEND 2:KX15JTQP001111112\n")
        response =  ser.readline()
        if(response[0:2] == "Rx"):
            if(counter == 100):
                ser.write("AT+SEND 2:KX15JTQP000020082\n") 
                print "##### RF : 92000000"
                print "##### Device Network Joined : 10"
                print "##### Device Kinds : LAMP"
                print "##### REGDATA : 2000"
                print "##### REGION : KR920"
                print "##### counter : ",counter
                print "Send Command... ",datetime.fromtimestamp(time.time())
                print "Receive Request... ",datetime.fromtimestamp(time.time())
                print "                    "
                ser.write("AT+SEND 2:KX15JTQP000020082\n")
                ser.write("AT+SEND 2:KX15JTQP000020082\n")
            else:
                ser.write("AT+SEND 2:KX15JTQP000020080\n")
                print "##### RF : 92000000"
                print "##### Device Network Joined : 10"
                print "##### Device Kinds : LAMP"
                print "##### REGDATA : 0"
                print "##### REGION : KR920"
                print "##### counter : ",counter
                print "Send Command... ",datetime.fromtimestamp(time.time())
                print "Receive Request... ",datetime.fromtimestamp(time.time())
                print "                    "
            counter = counter + 1
#        print response[0:2]
#        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
