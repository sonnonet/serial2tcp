#!/usr/bin/env python
# write by sonnonet 1.2Ver
# CO2 Rev 2.4
# THL Rev 1.6 Extenstion
# PH Rev 1.0 
# Serial to Mysql 

# Data Format
# CO2  Data0
# THL Temperature Data0, Humidity Data1, Illumination Data2, Battery Data3
import time
import sys
import tos
import datetime
import threading
import requests, json
from influxdb import InfluxDBClient as influxdb


AM_OSCILLOSCOPE = 0x93



url = 'http://127.0.0.1:4242/api/put?details'

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 2),
                             ('ch1', 'int', 2),
                             ('ch2', 'int', 2),
                             ],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()



while True:
    p = am.read()
    msg = OscilloscopeMsg(p.data)
    print p
####### ZLeak Sensor Logic ############
    print "ID:",msg.srcID, "seqNo:",msg.seqNo, "ch1:",msg.ch1, "ch2:",msg.ch2
    if (msg.ch1 > 4000):
      val1 = 0
    else:
      val1 = 1
      print "CH1 LEAK!!!"

    if (msg.ch2 > 4000):
      val2 = 0
    else:
      val2 = 1
      print "CH2 LEAK!!!"


    data = [{
        'measurement' : 'sensor',
        'tags': {
          'chId' : msg.srcID,
        },
        'fields': {
          'seqNo' : msg.seqNo,
          'ch1' : val1,
          'ch2' : val2,
        }

    }]

    print data

    client = None
    try:
      client = influxdb('localhost', 8086, 'root', 'root', 'leak')
    except Exception as e:
      print "Exception " + str(e)

    if client is not None:
      try: 
        client.write_points(data)
      except Exception as e:
        print "Exception write " + str(e)
      finally:
        client.close()

