import serial
import time
from datetime import datetime
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
#ser2 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#ser.close()
#ser.open()
#count =0 
#ser.write("testing")
#temperature = 26
#strTemp='20'
#intTemp =0
try:
    while 1:
        ser.write("AT+SEND 2:KX15JTQP000020080\n")
        ser.write("AT+SEND 2:KX15JTQP001111112\n")
        time.sleep(3)
        ser.write("AT+SEND 2:KX15JTQP000020083\n")
        ser.write("AT+SEND 2:KX16JTQP000020083\n")
       

# if(response[0:2] == "Rx"):
#        if(count >=5):
#            try:
#                response = ser2.readline()
#                strTemp = response[12:14] 
#                print "temperature : " + response[12:14]
#                print "humidity : " + response[27:29]
#                intTemp = int(strTemp)
#            except:
#                pass 
      
#            if(temperature <= intTemp):
#                ser.write("AT+SEND 2:KX15JTQP000020082\n") 
#                print "fire"
#            print "##### RF : 92000000"
#            print "##### Device Network Joined : 10"
#            print "##### Device Kinds : LAMP"
#                print "##### REGDATE : 2000"
#                print "##### REGION : KR920"
#                print "##### counter : ",counter
#                print "Send Command... ",datetime.fromtimestamp(time.time())
#                print "Receive Request... ",datetime.fromtimestamp(time.time())
#                print "                    "
#                ser.write("AT+SEND 2:KX15JTQP000020082\n")
#            else:
#                ser.write("AT+SEND 2:KX15JTQP000020080\n")
#            print "##### RF : 92000000"
#                print "##### Device Network Joined : 10"
#                print "##### Device Kinds : LAMP"
#                print "##### REGDATE : 0"
#                print "##### REGION : KR920"
#                print "##### counter : ",counter
#                print "Send Command... ",datetime.fromtimestamp(time.time())
#                print "Receive Request... ",datetime.fromtimestamp(time.time())
#                print "                    "
#        print response[0:2]
#        count = count + 1;
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
