from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])

consumer = KafkaConsumer('ride-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer: 
    single_value = json.loads((message.value).decode('utf-8'))
    print(single_value)
    es.index(index='ride-list', doc_type='rides', id=single_value['id'], body=single_value)
    es.indices.refresh(index="ride-list")