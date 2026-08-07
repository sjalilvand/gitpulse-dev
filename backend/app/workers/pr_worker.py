import json
from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from app.db.postgres import SessionLocal
from app.db.models.pull_request import PullRequest
from datetime import datetime

consumer_config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'pr-worker',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)
consumer.subscribe(['github.pull_requests.created'])

def process_pr(event: dict):
    db: Session = SessionLocal()
    try:
        existing = db.query(PullRequest).filter(PullRequest.github_pr_id == event['github_pr_id']).first()
        if existing:
            print(f"PR {event['number']} already exists, skipping.")
            return

        pr = PullRequest(
            repo_id=event['repo_id'],
            github_pr_id=event['github_pr_id'],
            number=event['number'],
            title=event['title'],
            body=event.get('body', ''),
            state=event['state'],
            author_username=event['author_username'],
            base_branch=event['base_branch'],
            head_branch=event['head_branch'],
            merged=event['merged'],
            merged_at=datetime.fromisoformat(event['merged_at']) if event['merged_at'] else None,
            closed_at=datetime.fromisoformat(event['closed_at']) if event['closed_at'] else None,
            created_at=datetime.fromisoformat(event['created_at']),
            updated_at=datetime.fromisoformat(event['updated_at']),
            additions=event.get('additions', 0),
            deletions=event.get('deletions', 0),
            changed_files=event.get('changed_files', 0),
        )
        db.add(pr)
        db.commit()
        print(f"Saved PR #{pr.number}")
    except Exception as e:
        db.rollback()
        print(f"Error saving PR: {e}")
    finally:
        db.close()

def start_pr_worker():
    print("PR worker started. Listening for events...")
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
        process_pr(event)
    consumer.close()