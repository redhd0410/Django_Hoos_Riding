from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])

consumer = KafkaConsumer('ride_listing', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], auto_offset_reset = "earliest")
for message in consumer: 
    es.index(index='listing_index', doc_type='rides', id=some_new_listing['id'], body=message)
    es.indices.refresh(index='listing_index')
