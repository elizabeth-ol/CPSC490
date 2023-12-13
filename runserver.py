#!/usr/bin/env python

from sys import argv, exit, stderr
from app import app

def main():

    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[1])
    except Exception:
        print('Port must be an integer.', file=stderr)
        exit(1)

#look at cert and key gen
    try:
        app.run(host="0.0.0.0", port=port, debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()

