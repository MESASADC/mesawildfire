#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class wrappers for implementation of functionality for the GeoJSON objects
defined in the Swordfish API.

Created on 08/06/2015 11:37:25 
@author: dhohls
"""
import json
import datetime
import pytz
import uuid

TIME_ZONE = 'Africa/Johannesburg'


class Observation():

    def __init__(self, output=None):
        self.observations = []
        self.output_file = output

    def log(self, message):
        print message

    def count(self):
        return len(self.observations)

    def add(self, observation):
        self.observations.append(observation)

    def save_to_file(self, observation=None, reset=False):
        """Save observations (JSON format) to output file."""
        if observation:
            data = [observation, ]
        else:
            data = self.observations
        if self.output_file:
            mode = 'w' if reset else 'a'
            try:
                with open(output_file, mode) as outfile:
                    for datum in data:
                        json.dump(datum, outfile)
                        outfile.write('\n')
            except: 
                self.log('Unable to save data to: %s' % output_file)

    def load_from_file(self, filename=None):
        """Load observations (JSON format) from file."""
        self.observations = []
        _filename = filename or self.output_file
        try:
            odf = open(_filename, 'r')
            for line in odf.readlines():
                observation = json.loads(line.strip('\n'))
                self.observations.append(observation)
            odf.close()
        except: 
            self.log('Unable to load data from: %s' % _filename)


class OM_Measurement(Observation):

    def __init__(self, **kwargs):
        if not len(kwargs.keys()):
            self.observation = {}
            return
        time_zone = kwargs.get('time_zone', TIME_ZONE)
        tz = pytz.timezone(time_zone)
        ppt = tz.localize(datetime.datetime.now()).isoformat()
        phenomenon_time = kwargs.get('phenomenon_time', ppt)
        units = kwargs.get('units', '')
        value = kwargs.get('value', None)
        date_time = kwargs.get('date_time', None)
        lon = kwargs.get('longitude', 0.0)
        lat = kwargs.get('latitude', 0.0)
        foi_id = kwargs.get('foi_id', '')  # place/thing being monitored
        observed_property = kwargs.get('observed_property', '')
        parameter_id = kwargs.get('parameter_id', str(uuid.uuid4()))
        procedure_id = kwargs.get('procedure_id', '')   # sensor - manufacturer ID
        procedure_name = kwargs.get('procedure_name', '')   # sensor - local name
        # validate (min requirements)
        if not value:
            raise ValueError('Parameter "value" must be set')
        if not foi_id:
            raise ValueError('Parameter "foi_id" must be set')
        if not observed_property:
            raise ValueError('Parameter "observed_property" must be set')
        if not procedure_id:
            raise ValueError('Parameter "procedure_id" must be set')
        if not date_time:
            raise ValueError('Parameter "date_time" must be set')
        # date conversion
        try:
            date_time = tz.localize(date_time).isoformat()
        except:
            pass

        self.observation = {
            "type": "OM_Measurement", 
            "phenomenonTime": phenomenon_time, 
            "result": { 
                "units": units, 
                "value": value
            }, 
            "featureOfInterest": {
                "geometry": {
                    "type": "Point", 
                    "coordinates": [lon, lat]
                },
                "type": "Feature",
                "properties": {
                    "id": foi_id
                }
            },
            "observedProperty": {
                "type": observed_property
            }, 
            "parameter": {
                "id": parameter_id
            },
            "procedure": {
                "type": "sensor", 
                "id": procedure_id, 
                "description": procedure_name
            }
        }
        """Example:
        {
            "type": "OM_Measurement", 
            "phenomenonTime": "2015-06-26T10:44:11.044824+02:00", 
            "result": {
                "units": "kW",
                "value": 101
            }, 
            "featureOfInterest": {
                "geometry": {
                    "type": "Point", 
                    "coordinates": ["28.280400", "-25.756686"]
                }, 
                "type": "Feature", 
                "properties": {
                    "id": "CSIR:PTA:44"
                }
            }, 
            "observedProperty": {
                "type": "active_load"
            }, 
            "parameter": {
                "id": "da424015-0b98-4f32-a4a1-369bb8bdcda3"
            }, 
            "procedure": {
                "type": "sensor",
                "id": "CPOWER:124",
                "description": "cPowerMeter"
            }
        }
        """

    def dict_obs_time(self, observation):
        """Create dict containing parameter (observedProperty type), datetime, 
        feature id (in properties), and result (value ,units) from the original
        observation dictionary.  
        
        Example result:
        {
            "observedProperty": {"type": "active_load"},
            "phenomenonTime": "2015-06-19T09:35:00+02:00",
            "result": {"units": "kW", "value": 127.2},
            "properties": {"id": "CSIR:CPT:C42"}
        }
        
        Works for a single variable and a single 'time' variable
        """
        output = {}
        FOI = observation.get('featureOfInterest')
        properties = FOI.get('properties')
        observed_property = observation.get('observedProperty')
        result = observation.get('result')
        phen_time = observation.get('phenomenonTime')
        output = {
            "observedProperty": observed_property,
            "phenomenonTime": phen_time,
            "result": result,
            "properties": properties
        }
        return output

    def list_obs_time(self, observation=None):
        """Create list of (id,parameter,datetime,value) tuples from observation dict
        
        Works for a single variable and a single 'time' variable
        """
        observation = observation or self.observation
        output = []
        if observation:
            FOI = observation.get('featureOfInterest')
            properties = FOI.get('properties')
            fid = properties.get('id')
            observed_property = observation.get('observedProperty')
            param_name = observed_property.get('type')
            result = observation.get('result')
            datum = result.get('value')
            _time = observation.get('phenomenonTime')
            #print 'DEBUG', _time, param_name   
            output.append((fid,param_name,_time,datum))
        return output

    def csv_obs_time(self, observation=None, titles=False):
        """Create string with "id,parameter,datetime,value" values per line"""
        observation = observation or self.observation
        result = ""
        if not observation:
            return result
        _list = self.list_obs_time(observation)
        for _tuple in _list:
            result += ",".join(unicode(x) for x in _tuple)
        return result


class CFObservation(Observation):
    pass


class CFSimpleObservation(CFObservation):

    def __init__(self, **kwargs):
        if not len(kwargs.keys()):
            self.observation = {}
            return

        time_zone = kwargs.get('time_zone', TIME_ZONE)
        tz = pytz.timezone(time_zone)
        ppt = tz.localize(datetime.datetime.now()).isoformat()
        phenomenon_time = kwargs.get('phenomenon_time', ppt)
        units = kwargs.get('units', '')
        value = kwargs.get('value', None)
        date_time = kwargs.get('date_time', None)
        lon = kwargs.get('longitude', 0.0)
        lat = kwargs.get('latitude', 0.0)
        foi_id = kwargs.get('foi_id', '')  # place/thing being monitored
        observed_property = kwargs.get('observed_property', None)
        parameter_id = kwargs.get('parameter_id', str(uuid.uuid4()))
        procedure_id = kwargs.get('procedure_id', '')   # sensor - manufacturer ID
        procedure_name = kwargs.get('procedure_name', '')   # sensor - local name
        # validate (min requirements)
        if not value:
            raise ValueError('Parameter "value" must be set')
        if not foi_id:
            raise ValueError('Parameter "foi_id" must be set')
        if not observed_property:
            raise ValueError('Parameter "observed_property" must be set')
        if not procedure_id:
            raise ValueError('Parameter "procedure_id" must be set')
        if not date_time:
            raise ValueError('Parameter "date_time" must be set')
        # date conversion
        try:
            date_time = tz.localize(date_time).isoformat()
        except:
            pass
        
        self.observation = {
            "type":"CF_SimpleObservation",
            "parameter": {
                "id": parameter_id
            },
            "phenomenonTime": phenomenon_time,
            "procedure": {
                "type": "Sensor",
                "id": procedure_id, 
            },
            "featureOfInterest":{
                "type": "Feature", 
                "geometry": {
                    "type":"Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": foi_id
                }
            },
            "observedProperty": {
                "type": "TimeSeries"
            },
            "result":{
                "dimensions": {
	                "time": 2
                },
                "variables": {
	                "time": {
	                    "dimensions":["time"], 
	                    "units":"isoTime"
	                },
	                observed_property: {
	                    "dimensions":["time"],
	                    "units": units
	                }
                },
                "data":{
	                "time": [date_time,],
	                observed_property: [value,]
                }
            }
        }

    def list_obs_time(self, observation=None):
        """Create list of (id,parameter,datetime,value) tuples from observation  dict
        
        Works for a single variable and a single 'time' variable
        """
        observation = observation or self.observation
        output = []
        if observation:
            FOI = observation.get('featureOfInterest')
            properties = FOI.get('properties')
            fid = properties.get('id')
            result = observation.get('result')
            data = result.get('data')
            variables = result.get('variables')
            _vars = variables.keys()
            param = None
            for _var in _vars:
                if _var == 'time':
                    _time = data.get(_var)
                else:
                    param = data.get(_var)
                    param_name = _var
            #print 'DEBUG', _time, param_name
            for i, datum in enumerate(param):
                output.append((fid,param_name,_time[i],datum))
        return output

    def csv_obs_time(self, observation=None, titles=False):
        """Create string with "id,parameter,datetime,value" values per line"""
        observation = observation or self.observation
        result = ""
        if not observation:
            return result
        _list = self.list_obs_time(observation)
        for _tuple in _list:
            result += ",".join(unicode(x) for x in _tuple)
        return result

