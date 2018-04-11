#!/usr/bin/env python3

import os
from uuid     import UUID  # for validation
from datetime import datetime, timezone

from dateutil.parser    import parse as parse_date
from klein              import Klein
from twisted.web.static import File

LINKS   = os.getenv('LINKS', './links.csv')
BASEDIR = os.getenv('BASEDIR', '.')
PORT    = int(os.getenv('PORT', '8585'))
BASEURL = os.getenv('BASEURL', '/')

class Fail(Exception): pass

def get_file_info(uuid):
    with open(LINKS) as f:
        for line in f:
            uuid_, path, expire = [ x.strip() for x in line.split(',') ]
            if uuid_ == uuid:
                expire = parse_date(expire)
                return path, expire
    raise Fail('uuid not found')

app = Klein()

with app.subroute(BASEURL) as app:
    @app.route('/<uuid>/<filename>', methods=['GET','HEAD'])
    def serve_files(request, uuid, filename):
        UUID(uuid)  # just create it to see if it validates
        path, expiry_date = get_file_info(uuid)
        if datetime.now(timezone.utc) > expiry_date: raise Fail('expired')
        if filename != os.path.basename(path): raise Fail('path does not match')
        return File(os.path.join(BASEDIR, path))

    @app.route('/<uuid>/<filename>/', methods=['GET','HEAD'], branch=True)
    def serve_dir(request, uuid, filename):
        return serve_files(request, uuid, filename)

    @app.handle_errors
    def handle_errors(request, failure):
        print('Fail:', failure.getErrorMessage())
        #failure.printBriefTraceback()
        return File.childNotFound

if __name__ == '__main__':
    app.run("localhost", PORT)
