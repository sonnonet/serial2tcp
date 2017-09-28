
# -*- coding: utf-8 -*-
# Author : Jeonghoonkang, github.com/jeonghoonkang

# Packet sniffer for site debugging by budge
# It is using serial parsing for TinyOS 2.1.1 packet, CTP is basic
# But, specially for the Yggdrasil packet parsing,
# which is developed based on TinyOS 2.1.1 and modified by Sonnonet in Korea
# in the start point, it needs hardware Kmote or Telosb compliant mote with proper Channel and Group ID
# The application in the mote is BASESTATION which located in ...TinyOS_Main_Dir/apps/Basestation
# Be careful not to use Basestation.15.4
# this SW has so long boring upgrades from 2003, now moved to Python world
# you can see the packet format and description in wwww.tinyospacket.com
# default baudrate is 115200, which is the defualt value in TinyOS-2.1.1

#import serial,os,time, datetime
#import sys
import struct
import datetime
import time
from time import strftime, localtime
import time
from datetime import datetime,timedelta
import requests
import json
from getURL import getLocalURL
import paho.mqtt.client as mqtt

global nid
#global url

nid = -1

#OpenTSDB_ADDRESS = "http://192.168.0.224:4242/api/put?details"
def on_log(client, userdata, level, buf):
    print(buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        mqtt_client.connected_flag=True
        print("Mqtt connected OK")
    else:
	print("Bad connection returned code=", rc)
        mqtt_client.loop_stop()
def on_disconnect(client, userdata, rc):
    print("client disconnected ok")
def on_publish(client, userdata, mid):
    print("mqtt publish=", mid)

mqtt.Client.connected_flag=False
mqtt_client = mqtt.Client("zigbeege.uuid.001",)
mqtt_client.on_log = on_log
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish
mqtt_client.connect("energy.openlab.kr",1883,600)
mqtt_client.loop_start()
def parseDB(_pckt):
    global nid
    global url
    #check getURL.py file for exact same IP address of OpenTSDB
    url = getLocalURL()
    #url = OpenTSDB_ADDRESS
    #print url
    

    # packet_type is a number which sensor value of this packet including
    # such as Temperature, Humidity, Power, Light, and so on.
    packet_type = int(_pckt[22:24],16)
    _str_Type = retTosType(packet_type)
    print _str_Type
    if (_str_Type == 'None'):
        print "  " + _pckt
        print "  " + _pckt[0:20] + "              " , _pckt[36:40]
        return

    #print "  TOS packet type %d, 0x%X " %(packet_type, packet_type) , _str_Type

    _pckid = int(_pckt[36:40],16)
    nid = _pckid
    
    print "  node ID = %d, 0x%X" %(_pckid, _pckid)
    if ( 'THL' in _str_Type ):
#        _ibattery = savebattery(_battery)

        _temp = int(_pckt[48:52],16)
        _temp = (-39.6) + (_temp*0.01)
#        _rtemp = savetemp(_temp)
        #print ">>> (Value) Temperature = %.2f " %(_rtemp)
        _humi = int(_pckt[52:56],16)
#		_humi = savehumi(_humi)
        _humi = -2.0468 + (0.0367*_humi) + (-1.5955*0.000001) * _humi * _humi
        _battery = int(_pckt[44:48],16)
        print _battery
        savetemp(_temp, _humi, _battery)
		

    elif ( 'CO2' in _str_Type ):
        _co2 = int(_pckt[48:52],16)
        _co2 = saveco2(_co2)

    elif ( 'SPlug' in _str_Type ):
        _watt = _pckt[54:60]
        _watt = savesplug(_watt)

    elif ( 'Etype' in _str_Type ):
        _c = _pckt[48:56]
        _t = _pckt[64:72]

        _c_swp = '"'+'\\x'+_c[2:4]+'\\x'+_c[0:2]+'\\x'+_c[6:8]+'\\x'+_c[4:6]+'"'
        _t_swp = '"'+'\\x'+_t[2:4]+'\\x'+_t[0:2]+'\\x'+_t[6:8]+'\\x'+_t[4:6]+'"'

        _etype_current, _etype_total = saveetype(_c_swp, _t_swp)
        #print "    >>> (Value) Current Watt = %.2f, Total Watt = %s " %(_etype_current, _etype_total)

    else:
        pass

    #closing packet print
    print ' ', '-' * 90

def savetemp(_temp, _humi, _battery) :
#    _ftemp = (-39.6) + (_temp*0.01)
    otsdb_restful_put(_temp, _humi, _battery, nid)
#    print ("temp : " + str(_ftemp))
    return _temp

def savehumi(_humi) :
    _fhumi = -2.0468 + (0.0367*_humi) + (-1.5955*0.000001) * _humi * _humi
    otsdb_restful_put('humi', _fhumi, nid)
    print ("humi : "+ str(_fhumi))
    return _fhumi

def saveillumi(_illumi) :
    _fillumi = (_illumi * 100) / 75;
    _fillumi = _fillumi * 10;
    otsdb_restful_put('illumi', _fillumi, nid)
    print ("lux : " + str(_fillumi))
    return _fillumi

def savebattery(_battery) :
    otsdb_restful_put("battery", _battery, nid)
    print ("battery : " + str(_battery))
    return _battery

def saveco2(_co2) :
    _fco2 = (_co2 * 3300) / 16384
    otsdb_restful_put('co2', _fco2, nid)
    print _fco2
    return _fco2

def savesplug(_watt) :
    rawData = _watt
    tmp = bigEndian(rawData)
    if tmp > 15728640:
	tmp =0
    else:
	tmp=float(tmp/4.127/10)
        _watt = tmp
    print " watt: %.2f" %(_watt)
    otsdb_restful_put('watt', _watt, nid)
    return _watt

def saveetype(_c, _t) :
    #assert len(_c) == 8
    #assert len(_t) == 8
    try :
        _c = eval(_c)
        _c_tmp = struct.unpack('i',_c)[0]
        _c_val = _c_tmp
        _t = eval(_t)
        _t_val = struct.unpack('f',_t)[0]
    #_t_val = "%.2f" %_t_val

    except (ValueError, SyntaxError):
        print " "*10, " sometimes SyntaxError occurs @ eval(_t)"
        return (-1, -1)

    # check it is opposite with manual
    # i exchange c value and t value
    otsdb_restful_put('power', _t_val, nid)
    otsdb_restful_put('t_power', _c_val, nid)
    return _t_val, _c_val


def retTosType(packet_type):
    if (packet_type is 100) : #0x64
        return 'THL mote'
    elif (packet_type is 99) :
        return 'Base mote'
    elif (packet_type is 101) : #0x65
        return 'PIR mote'
    elif (packet_type is 102) : #0x66
        return 'CO2 mote'
    elif (packet_type is 109) : #0x6d
        return 'SPlug mote'
    elif (packet_type is 211) : #0xd3
        return 'Etype mote'
    elif (packet_type is 250) : #0xfa
        return 'Routing info'
    else :
        return 'None'

    print "  type of packet_type variable =", type(packet_type)

 #    if packet_type == '70' : # this is TH20 sensor, Total sensor
 #        if debug == 1 :
 #            timePrint()
 #            print packet, "len =", len(packet)/2
 #        sht2x_str = packet[-10:-8]
 #        nodeid_str = packet[39:40]
 #        seq_num = packet[41:44]
 #        sht2x_decimal = int(sht2x_str,16) # convert STR, 16-base to decimal INT
 #        #print "type=", type(sht2x_decimal), sht2x_decimal
 #        temperature = 175.72 * sht2x_decimal / pow(2,16) - 46.85
 #        #tmp_humi = 125 * float(humi) / pow(2,16) - 6
 #        print " >>>> ", sht2x_decimal, hex(sht2x_decimal), temperature,
 #        nodeid_str, seq_num

def showtypes():
    print '\n ', '-' * 90
    print "   99, 0x63 Base mote    |  100, 0x64 THL "
    print "  101, 0x65 PIR  mote    |  102, 0x66 CO2 "
    print "  103, 0x67 VOC  mote    |  104, 0x68 Splug"
    print "  105, 0x69 sonic mote   |  106, 0x70 Thermo"
    print "  107, 0x71 ELT CO2 mote |  108, 0x72 Splug2"
    print "  211, 0xD3 Etype mote   |  "
    print ' ', '-' * 90

def bigEndian(s):
	res = 0
	while len(s):
		s2 = s[0:2]
	        s = s[2:]

		res <<=8
		res += eval('0x' + s2)
	return res


def otsdb_restful_put(_temp, _humi, _battery, nid):


#    if stype is "temp" :
#        m = "rc01.temp.degree"
#    elif stype is "humi" :
#        m = "rc01.humi.persent"
#    elif stype is "battery" :
#        m = "rc01.battery.mah"
#    elif stype is "illumi" :
#        m = "rc01.illumi.lux"
#    elif stype is "power" :
#        m = "rc01.power.W"
#    elif stype is "t_power" :
#        m = "rc01.t_power.WH"
#    elif stype is "watt" :
#        m = "rc01.t_watt.W"
#    elif stype is "co2" :
#        m = "rc01.co2.ppm"
#    else :
#        print " m is empty "
#        return
    nid = int(nid) + 30
    #print "  " + " ---> logging to open TSDB,   " + m + " " + str(r) + " " + nid
    datetime_now = datetime.now()
    data = {
        "Status": "On",
		"TrainID": "104",
		"SensorName": "TempHum",
		"temp": _temp,
		"hum": _humi,
        "timestamp": str(datetime_now),
#        "value": r,
#        "tags": {
        "SensorID" : nid
#            "sensor" : stype,
#	    "floor_room": "SG_office",
#	    "building": "SG",
#	    "owner": "kang",
#	    "country": "kor"
        }
    print data

    mqtt_client.publish("/keti/energy/fromgw", json.dumps(data), qos=1)
	# tags should be less than 9, 8 is alright, 9 returns http error
        # empty string not allowed.
#    }

#    try :
#        ret = requests.post(url, data=json.dumps(data))
        #print "  ***** HTTP post return : " + ret.text
        #print "  ***** "

#    except requests.exceptions.Timeout :
        #logger.error("  **** error : http connection error, Timeout  %s", ret)
#        pass
#    except requests.exceptions.ConnectionError :
        #logger.error("  **** error : http connection error, Too many requests %s")
#        pass

#    return
