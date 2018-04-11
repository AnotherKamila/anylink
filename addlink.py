#!/usr/bin/env python3

import os
import sys
from uuid import uuid4
from datetime import datetime, timedelta

DEFAULT_EXPIRE_DAYS=30

def add_file(path, expire_days=DEFAULT_EXPIRE_DAYS, never_expire=False):
    key    = str(uuid4())
    expire = (datetime.now() + timedelta(days=expire_days)).isoformat()
    if never_expire: expire = None
    with open('./links.csv', 'a') as f:
        f.write('{}, {}, {}\n'.format(key, path, expire))
    return key

if __name__ == '__main__':
    # TODO args validation
    path = sys.argv[1]
    expire = int(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_EXPIRE_DAYS
    print('{}/{}'.format(add_file(path, expire, expire == 0), os.path.basename(path)))
