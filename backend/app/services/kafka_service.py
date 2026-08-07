from confluent_kafka import Producer
import json
from app.core.config import get_settings

settings = get_settings()

producer_config = {
    'bootstrap.servers': settings.kafka_bootstrap_servers
}
producer = Producer(producer_config)

def send_event(topic: str, key: str, value: dict):
    try:
        producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(value),
            callback=delivery_report
        )
        producer.flush()
    except Exception as e:
        print(f"Failed to send event to Kafka: {e}")

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")