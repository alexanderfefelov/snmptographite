#!/usr/bin/python

import ecks
import graphitesend
import os
import yaml

with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'snmptographite.yml', 'r') as yml_file:
    config = yaml.load(yml_file)

graphite_config = config['graphite']

snmp_engine = ecks.Ecks()
graphite_engine = graphitesend.init(graphite_server=graphite_config['host'], graphite_port=graphite_config['port'],
                                    prefix='', system_name='')

for device_config in config['devices']:
    host = device_config['host']
    community = device_config['community']
    result = []
    for metric_config in device_config['metrics']:
        oid = tuple(map(int, metric_config['oid'].split('.')))
        name = metric_config['name']
        data = snmp_engine.get_snmp_data(host, community, oid, True)
        if data:
            value = data[0][2]
            result.append((name, value))
    graphite_engine.send_list(result)
