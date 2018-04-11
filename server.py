#!/usr/bin/env python3

import os
from uuid     import UUID  # for validation
from datetime import datetime

from dateutil.parser    import parse as parse_date
from klein              import route, run, handle_errors
from twisted.web.static import File

LINKS   = os.getenv('LINKS', './links.csv')
BASEDIR = os.getenv('BASEDIR', '.')
PORT    = int(os.getenv('PORT', '8585'))

class Fail(Exception): pass

def get_file_info(uuid):
    with open(LINKS) as f:
        for line in f:
            uuid_, path, expire = [ x.strip() for x in line.split(',') ]
            if uuid_ == uuid:
                expire = parse_date(expire)
                return path, expire
    raise Fail('uuid not found')

@route('/<uuid>/<filename>', methods=['GET','HEAD'])
def serve_files(request, uuid, filename):
    UUID(uuid)  # just create it to see if it validates
    path, expiry_date = get_file_info(uuid)
    if datetime.now(timezone.utc) > expiry_date: raise Fail('expired')
    if filename != os.path.basename(path): raise Fail('path does not match')
    return File(os.path.join(BASEDIR, path))

@handle_errors
def handle_errors(request, failure):
    print('Fail:', failure.getErrorMessage())
    #failure.printBriefTraceback()
    request.setResponseCode(404)
    return "404, that's all I'll tell ya"

if __name__ == '__main__':
    run("localhost", PORT)
