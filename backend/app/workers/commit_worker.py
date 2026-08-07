import json
import threading
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from app.db.postgres import SessionLocal
from app.db.models.commit import Commit
from datetime import datetime

consumer_config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'commit-worker',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)
consumer.subscribe(['github.commits.created'])

def process_commit(event: dict):
    db: Session = SessionLocal()
    try:
        # چک کنیم commit_hash قبلاً وجود نداشته باشد
        existing = db.query(Commit).filter(Commit.commit_hash == event['commit_hash']).first()
        if existing:
            print(f"Commit {event['commit_hash']} already exists, skipping.")
            return

        commit = Commit(
            repo_id=event['repo_id'],
            commit_hash=event['commit_hash'],
            author_name=event['author_name'],
            author_email=event['author_email'],
            author_username=event['author_username'],
            message=event['message'],
            branch=event.get('branch', 'main'),
            commit_url=f"https://github.com/{event['repo_full_name']}/commit/{event['commit_hash']}",
            committed_at=datetime.fromisoformat(event['committed_at']),
            additions=event.get('additions', 0),
            deletions=event.get('deletions', 0),
            files_changed=event.get('files_changed', 0),
        )
        db.add(commit)
        db.commit()
        print(f"Saved commit {commit.commit_hash}")
    except Exception as e:
        db.rollback()
        print(f"Error saving commit: {e}")
    finally:
        db.close()

def start_worker():
    print("Commit worker started (inside backend). Listening for events...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        event = json.loads(msg.value().decode('utf-8'))
        process_commit(event)
    consumer.close()