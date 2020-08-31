#!/usr/bin/python3
#
# Copyright (c) 2018 Sinbinet Corp.
# All rights reserved.
#
# author Suchang Lee <suchanglee@sinbinet.com>
# author Sukun Kim <sukunkim@sinbinet.com>


import datetime
import logging
from influxdb import InfluxDBClient as influxdb

from influxdbConsts import influxdbConsts as InfluxdbConsts
from sensorConsts import sensorConsts as SensorConsts


class influxdbDataMgr:
  def __init__(self, host, port, user, passwd, db):
    self.logger = logging.getLogger('sensing.dataMgr.influxdb')

    self.host = host
    self.port = port
    self.user = user
    self.passwd = passwd
    self.db = db


  def write(self, value):
    client = None

    try:
      client = influxdb(self.host, self.port, self.user, self.passwd, self.db,
        timeout = InfluxdbConsts.INFLUXDB_WRITE_TIMEOUT, 
        retries = InfluxdbConsts.INFLUXDB_WRITE_RETRIES)
    except Exception as e:
      self.logger.warn('open Exception ' + str(e))

    if client is not None:
      try: 
        client.write_points(self.setData(value))
      except Exception as e:
        self.logger.warn('write Exception ' + str(e))
      finally:
        client.close()
  

  def setData(self, value):
    data = []

    try:
      for sensor in value['sensor']:
        try:
          datum = {
            'measurement' : 'sensor_data_moving_history',
            'tags': {
              'SensorId' : value['SensorId'],
              'SensorSerialId': value['SensorSerialId'],
              'SensorType' : sensor['SensorType'],
              'VehicleId' : value['VehicleId'],
              'ZoneId' : sensor['ZoneId'],
            },
            'fields': {
              'record_id' : value['record_id'],
              'SeqNo' : value['SeqNo'],
              'TTL' : value['TTL'],
              'SnapshotSeqNo' : value['SnapshotSeqNo'],
            }
          }

          fields = datum['fields']

          if sensor['SensorType'] == SensorConsts.SENSING_SENSOR_TYPE_DUMMY:
            fields['SensorData0'] = sensor['SensorData']['value']
    
          elif sensor['SensorType'] == SensorConsts.SENSING_SENSOR_TYPE_T200:
            fields['SensorData0'] = sensor['SensorData']['co2']
            fields['SensorData1'] = sensor['SensorData']['ttl']
    
          elif sensor['SensorType'] == \
            SensorConsts.SENSING_SENSOR_TYPE_HPMA115S0:
            fields['SensorData0'] = sensor['SensorData']['pm2_5']
            fields['SensorData1'] = sensor['SensorData']['pm10']

          elif sensor['SensorType'] == SensorConsts.SENSING_SENSOR_TYPE_MT3337:
            fields['SensorData0'] = sensor['SensorData']['datetime']
            fields['SensorData1'] = sensor['SensorData']['latitude']
            fields['SensorData2'] = sensor['SensorData']['longitude']
            fields['SensorData3'] = sensor['SensorData']['speed']
            fields['SensorData4'] = sensor['SensorData']['COG']
            fields['SensorData5'] = sensor['SensorData']['ttl']

          elif sensor['SensorType'] == SensorConsts.SENSING_SENSOR_TYPE_SDS021:
            fields['SensorData0'] = sensor['SensorData']['pm2_5']
            fields['SensorData1'] = sensor['SensorData']['pm10']
            fields['SensorData2'] = sensor['SensorData']['ttl']

          else:
            continue
    
        except Exception as e:
          self.logger.error('setData datum Exception ' + str(e))

        data.append(datum)

    except Exception as e:
      self.logger.error('setData data Exception ' + str(e))

    return data
