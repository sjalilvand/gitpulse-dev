import json
from confluent_kafka import Consumer, KafkaError
from app.services.analytics_service import insert_commit_analytic, insert_issue_analytic

consumer_config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'analytics-worker-pg',
    'auto.offset.reset': 'earliest',
}

def start_analytics_worker():
    consumer = Consumer(consumer_config)
    consumer.subscribe(['github.commits.created', 'github.issues.created'])
    print("Analytics worker subscribed to commit and issue topics. Writing to PostgreSQL...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Kafka error: {msg.error()}")
                break
        event = json.loads(msg.value().decode('utf-8'))
        topic = msg.topic()
        try:
            if topic == 'github.commits.created':
                insert_commit_analytic(event)
            elif topic == 'github.issues.created':
                insert_issue_analytic(event)
        except Exception as e:
            print(f"Error in analytics worker: {e}")
    consumer.close()