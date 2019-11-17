# Subreddit Pattern


# Concurrency Notes

Multiple instances of ingesting in the subreddit pattern can be run concurrently while all sharing the same database configuration. Typically these instances should be configured to collect data from distinct subreddits but failure to do this does not violate of the database and only results in significant duplicate work.


# Required SQL Tables

Running a ingestion service in the subreddit pattern requires three tables which need to be set in the configuration.


1. `$submission_table`: This table is used to determine the time bounds on the next working block and is the sink for all the reddit submissions ingested. This table should have the following schema:
```
submission_id VARCHAR(16) NOT NULL PRIMARY KEY,
creation_datetime DATETIME,
retrieval_datetime DATETIME,
score MEDIUMINT UNSIGNED,
num_comments MEDIUMINT UNSIGNED,
author_name VARCHAR(128),
author_id VARCHAR(16),
upvote_ratio FLOAT(3,2),
url TEXT,
permalink VARCHAR(512),
subreddit_name VARCHAR(128),
subreddit_id VARCHAR(16),
title VARCHAR(512),
text TEXT
```

2. `$comment_table`: This table stores all the comments associated with the submissions stored in `$submission_table`. This table should have the following schema:
```
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
```

# Configuration

Running the reddit collection service in the subreddit pattern is done by setting the `pattern: subreddit` in the general service configuration. In addition, this pattern admits the following pattern configuration flags:

* `left_bound: <int>`:
* `subreddit: <str>`:
* `submission_table: <str>`:
* `comment_table: <str>`:


# API

The subreddit pattern supports the general `/get_queue` and `/push` endpoints of the general reddit collection service. Supported parameters for the `/push` endpoint are as follows:

* `limit: <int>`:
* `before: <int>`:
* `after: <int>`:

It is valid to provide a `limit` argument *or* both the `before` and `after` argument.
