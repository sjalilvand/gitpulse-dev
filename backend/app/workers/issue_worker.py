import json
import time
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from app.db.postgres import SessionLocal
from app.db.models.issue import Issue
from datetime import datetime

TOPIC = 'github.issues.created'
consumer_config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'issue-worker-v2',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
}

def process_issue(event: dict):
    db: Session = SessionLocal()
    try:
        existing = db.query(Issue).filter(Issue.github_issue_id == event['github_issue_id']).first()
        if existing:
            print(f"Issue #{event['number']} already exists, skipping.")
            return
        issue = Issue(
            repo_id=event['repo_id'],
            github_issue_id=event['github_issue_id'],
            number=event['number'],
            title=event['title'],
            body=event.get('body', ''),
            state=event['state'],
            author_username=event['author_username'],
            labels=event.get('labels', ''),
            created_at=datetime.fromisoformat(event['created_at']),
            updated_at=datetime.fromisoformat(event['updated_at']),
            closed_at=datetime.fromisoformat(event['closed_at']) if event['closed_at'] else None,
        )
        db.add(issue)
        db.commit()
        print(f"Saved issue #{issue.number}")
    except Exception as e:
        db.rollback()
        print(f"Error saving issue: {e}")
    finally:
        db.close()

def start_issue_worker():
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPIC])
    print(f"Issue worker subscribed to {TOPIC}. Polling...")

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    print(f"Topic {TOPIC} not yet available, retrying...")
                    time.sleep(2)
                    # unsubscribe and resubscribe to force metadata refresh
                    consumer.unsubscribe()
                    consumer.subscribe([TOPIC])
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break
            event = json.loads(msg.value().decode('utf-8'))
            process_issue(event)
        except Exception as e:
            print(f"Unexpected error in worker loop: {e}")
            time.sleep(5)
    consumer.close()