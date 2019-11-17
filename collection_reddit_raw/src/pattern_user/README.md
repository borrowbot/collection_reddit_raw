# User Pattern


# Concurrency Notes
A user pattern ingestion service is global in nature and thus there is not a natural use case for running multiple instances simultaneously.

When ingesting using a user pattern in conjunction with subreddit pattern ingestion services, the `$submission_table` and `$comment_table` tables for the user pattern ingestion service must be distinct from those two tables used in the subreddit ingestion service, though instances of the subreddit ingestion services can share tables.


# Required SQL Tables

Running a ingestion service in the user pattern requires three configurable tables which need to be set in the configuration. These tables should have the same schema as is documented in the subreddit pattern documentation though note that the tables themselves must be distinct (see the concurrency notes above):


1. `$submission_table`: This table, along with `$comment_table` are used to determine the time bounds on the next working block. These two tables are also the sinks that parsed data is written to.

2. `$comment_table`: See notes for `$submission_table` above.


# Configuration

Running the reddit collection service in the subreddit pattern is done by setting the `pattern: user` in the general service configuration. In addition, this pattern admits the following pattern configuration flags:

* `left_bound: <int>`:
* `submission_table: <str>`:
* `comment_table: <str>`:
* `reference_submission_table: <str>`:
* `reference_comment_table: <str>`:


# API

The subreddit pattern supports the general `/get_queue` and `/push` endpoints of the general reddit collection service. The `/push` endpoint has a single required integer parameter `interval` which specifies the time size in seconds of the block of comments and submissions to ingest.
