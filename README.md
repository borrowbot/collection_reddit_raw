A flask based data collection service which can be used to ingest and maintain a historical database of reddit posts and comments from a single subreddit.


# Data Quality Assurances

The service, once started ingests data from starting from 2010-01-01 in ascending order. So long as the service is not interrupted during ingestion, the service ensures a temporally contiguous block of data with no duplication even between service restarts.


# Concurrency Requirements

Each instance of service is blocked to a single ingestion request at a time. Additional requests will be blocked until the currently executing one is completed.

Running multiple instances of this service is okay only for ingestion of data from disjoint subreddits.


# Setting Configuration

A blank configuration file is provided in `collection_reddit_raw/resources/config.yml`. See the PRAW documentation for guidance on configuring the reddit portion of the configuration file.


# Creating SQL Tables

Create a new SQL database making sure to set default encoding to `utf8mb4` or else ingestion will fail on encountering a 4-byte unicode character. For instance:

```
CREATE DATABASE redditdatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Two tables are required in this database and should be created with the following specification:

```
CREATE TABLE submissions (
  submission_id VARCHAR(16) NOT NULL PRIMARY KEY,
  creation_datetime DATETIME,
  retrieval_datetime DATETIME,
  score MEDIUMINT UNSIGNED,
  num_comments MEDIUMINT UNSIGNED,
  author_name VARCHAR(128),
  author_id VARCHAR(16),
  upvote_ratio FLOAT(3,2),
  url VARCHAR(512),
  permalink VARCHAR(512),
  subreddit_name VARCHAR(128),
  subreddit_id VARCHAR(16),
  title VARCHAR(512),
  text TEXT
);
```

```
CREATE TABLE comments (
  comment_id VARCHAR(16) NOT NULL PRIMARY KEY,
  creation_datetime DATETIME,
  retrieval_datetime DATETIME,
  score MEDIUMINT,
  subreddit_name VARCHAR(128),
  subreddit_id VARCHAR(16),
  text TEXT,
  author_name VARCHAR(128),
  author_id VARCHAR(16),
  parent_id VARCHAR(16),
  link_id VARCHAR(16)
);
```


# Building and Running in Docker

To build the docker container, first build the [baseimage](https://github.com/borrowbot/baseimage) with the following command:

```
docker build . -t baseimage_borrowbot
```

Then, the DockerFile here can be built with:

```
docker build . -t collection_reddit_raw
```

The service can be run with:

```
docker run -d --network=host collection_reddit_raw
```


# Using the API
