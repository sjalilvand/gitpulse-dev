CREATE DATABASE IF NOT EXISTS gitpulse_analytics;

USE gitpulse_analytics;

CREATE TABLE IF NOT EXISTS commit_events (
    event_id String,
    repo_id UInt32,
    repo_full_name String,
    commit_hash String,
    author_username String,
    branch String,
    message String,
    additions UInt32,
    deletions UInt32,
    files_changed UInt32,
    committed_at DateTime,
    ingested_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (repo_id, committed_at, author_username);

CREATE TABLE IF NOT EXISTS issue_events (
    event_id String,
    repo_id UInt32,
    repo_full_name String,
    issue_number UInt32,
    title String,
    state String,
    author_username String,
    category String,
    priority String,
    created_at DateTime,
    closed_at Nullable(DateTime),
    ingested_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (repo_id, created_at);