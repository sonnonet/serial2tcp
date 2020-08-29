#!/usr/bin/env python
# write by HanGyeol 0.9_Ver
# Sensor to Kmote with Lora

# Data Format
# LedColor Control  Data0
# Data0 = 0x00 White On 
# Data0 = 0x01 White toggle
# Data0 = 0x02 RED toggle
# Data0 = 0x03 Green toggle
# Data0 = 0x04 Blue toggle

import serial
import sys
import tos
import datetime
import threading


AM_OSCILLOSCOPE = 0x93
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=3)


class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 2),
                             ('type', 'int', 2),
                             ('Data0', 'int', 1),
                             ('Data1', 'int', 1),
                             ('Data2', 'int', 1),
                             ('Data3', 'int', 1),
                             ('Data4', 'int', 1),
                             ],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()


while True:
    p = am.read()
    msg = OscilloscopeMsg(p.data)
    print msg.Data0
####### LoRa Led Control Logic ############
    if msg.Data0 == 0:
        ser.write("AT+SEND 2:KX15JTQP000020080\n")
        print "Led White On"
    elif msg.Data0 == 1:
        ser.write("AT+SEND 2:KX15JTQP000020081\n")
        print "Led White toggle"
    elif msg.Data0 == 2:
        ser.write("AT+SEND 2:KX15JTQP000020082\n")
        print "Led Red toggle"
    elif msg.Data0 == 3:
        ser.write("AT+SEND 2:KX15JTQP000020083\n")
        print "Led Green toggle"
    elif msg.Data0 == 4:
        ser.write("AT+SEND 2:KX15JTQP000020084\n")
        print "Led Blue toggle"
    else:
        ser.write("AT+SEND 2:KX15JTQP000020080\n")
        print "default Led White On"
