from kafka import KafkaConsumer

consumer = KafkaConsumer('click-topic', group_id='ride-indexer', bootstrap_servers=['kafka:9092'])

while(True):
    sleep(0.1)    
    for message in consumer: 
        click = json.loads((message.value).decode('utf-8'))
        user=click['user']
        item=click['id']
        f= open("access.log","a")
        f.write(user + '\t' + item + '\n')