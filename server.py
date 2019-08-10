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
    else if pattern == 'user':
        from collection_reddit_raw.src.pattern_user.server import server
    else:
        raise Exception("invalid pattern in service configuration")

    server.run(port=CONFIG['port'])


if __name__ == '__main__':
    main()
