import csv
import os
import requests
from pykafka import KafkaClient

sample_file = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2016-01.csv"
kafka_brokers = os.getenv("KAFKA_BROKERS", "localhost:9092")
kafka_topic = os.getenv("KAFKA_TOPIC", "test")


client = KafkaClient(hosts=kafka_brokers)
topic = client.topics[kafka_topic.encode("utf8")]
producer = topic.get_producer()


if not os.path.isfile(sample_file):
  url = sample_file
  response = requests.get(url, stream=True)

  for data in response.iter_lines():
    producer.produce(data)
