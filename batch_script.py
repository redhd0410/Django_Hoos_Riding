from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

from time import sleep

es = Elasticsearch(['es'])

consumer = KafkaConsumer('ride-listings-topic', group_id='ride-indexer', bootstrap_servers=['kafka:9092'], api_version='0.9')

while(True):
    sleep(0.1)    
    for message in consumer: 
        single_value = json.loads((message.value).decode('utf-8'))
        print(single_value)
        es.index(index='ride-list', doc_type='rides', id=single_value['id'], body=single_value)
        
        es.indices.refresh(index="ride-list")