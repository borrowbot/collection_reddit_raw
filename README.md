A flask based data collection service which can be used to ingest and maintain a historical database of reddit posts and comments from a single subreddit. This service template implements a number of different ingestion patterns which can be used together to gather a complete set of historical data for analysis.

# Setting Configuration

Before running this service, a configuration file template found at `collection_reddit_raw/resources/config.yml` needs to be set. The configuration has a general section at the top that is used to set the ingestion pattern and some other globally applicable configuration. Depending on the ingestion pattern used, further configuration is probably necessary - templates for each ingestion pattern can be found commented out in the configuration template. See the ingestion pattern specific documentation for more details.

# SQL Requirements

Projects built on this service write parsed submissions and comments to a MySQL database. Though the specific tables required for different ingestion patterns can vary (documented in each pattern's respective documentation), the database these tables reside in must be set to a default encoding to `utf8mb4` or else ingestion will fail on encountering a 4-byte unicode character. For instance:

```
CREATE DATABASE redditdatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

# Building Containers with Docker

This ingestion service runs in a Docker container for dependency management. Before building the service itself, you need to first build the docker base image we've provided [here](https://github.com/project-earth/baseimage). Afterwards, the image for the ingestion service itself and be built and run.
