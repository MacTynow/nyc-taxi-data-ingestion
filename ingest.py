import csv
import os
import requests
import json
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

  for line in response.iter_lines():
    if len(line) > 10:
      data = {}
      data["pickup_time"] = line.split(",")[1]
      data["dropoff_time"] = line.split(",")[2]
      data["pickup_long"] = line.split(",")[5]
      data["pickup_lat"] = line.split(",")[6]
      data["dropoff_long"] = line.split(",")[9]
      data["dropoff_lat"] = line.split(",")[10]
      json_data = json.dumps(data)
      producer.produce(json_data)
