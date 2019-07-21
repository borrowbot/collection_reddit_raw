import json
import threading
from flask import request

from baseimage.config import CONFIG


VALID_PATTERNS = ['subreddit', 'user']


def main():
    pattern = CONFIG['pattern']
    assert pattern in VALID_PATTERNS

    if pattern == 'subreddit':
        from collection_reddit_raw.src.pattern_subreddit.server import server

    server.run(port=CONFIG['port'])


if __name__ == '__main__':
    main()
