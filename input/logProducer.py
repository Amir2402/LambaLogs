from sys import stdin
from kafka import KafkaProducer 
import json 

BROKERS = ['kafka-borker-1:9092', 'kafka-broker-2:9093'] 
TOPIC_NAME = "logTopic" 

def create_Producer(brokers):
    logProducer = KafkaProducer(bootstrap_servers = brokers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    return logProducer

def readLogs(brokers): 
    logProducer = create_Producer(brokers) 

    try: 
        for line in stdin: 
            record = json.loads(line)
            
            if record["method"] in ("POST", "GET"): 
                logProducer.send(topic = TOPIC_NAME, key = "0".encode(), value = record, partition = 0)
            
            else: 
                logProducer.send(topic = TOPIC_NAME, key = "1".encode(), value = record, partition = 1)
    except: 
        print("Stream ended or error occured") 

readLogs(BROKERS) 
