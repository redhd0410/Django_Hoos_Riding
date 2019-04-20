from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

from time import sleep

es = Elasticsearch(['es'])

with open('./models/db.json') as data:
    json_data = json.load(data)

    for line in json_data:
        if line['model'] == 'models.user':
            print('This is a user: ' + str(line))
            es.index(index='user-list', doc_type='users', id=line['pk'], body=line)
            es.indices.refresh(index="user-list")
            print('Indexed it to Elasticsearch!')
        elif line['model'] == 'models.vehicle':
            print('This is a vehicle: ' + str(line))
            es.index(index='vehicle-list', doc_type='vehicles', id=line['pk'], body=line)
            es.indices.refresh(index="vehicle-list")
            print('Indexed it to Elasticsearch!')
        elif line['model'] == 'models.ride':
            print('This is a ride: ' + str(line))
            es.index(index='ride-list', doc_type='rides', id=line['pk'], body=line)
            es.indices.refresh(index="ride-list")
            print('Indexed it to Elasticsearch!')
        elif line['model'] == 'models.authenticator':
            print('This is an authenticator: ' + str(line))
            es.index(index='auth-list', doc_type='auths', id=line['pk'], body=line)
            es.indices.refresh(index="auth-list")
            print('Indexed it to Elasticsearch!')
        

consumer = KafkaConsumer('ride-listings-topic', group_id='ride-indexer', bootstrap_servers=['kafka:9092'], api_version='0.9')

while(True):
    sleep(0.1)    
    for message in consumer: 
        single_value = json.loads((message.value).decode('utf-8'))
        print(single_value)
        es.index(index='ride-list', doc_type='rides', id=single_value['id'], body=single_value)
        es.indices.refresh(index="ride-list")
