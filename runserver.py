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











# from sys import exit, stderr
# from app2 import app
# import flask
# import argparse




# parser = argparse.ArgumentParser(description='The registrar application')
# parser.add_argument('port', type=int, nargs=1,
#                     help='the port at which the server should listen')

# def main():
#     # args = parser.parse_args()
#     # port = vars(args)["port"][0]
#     port = 3000
#     try:
#         app.run(host='0.0.0.0', port=port, debug=True)
#     except Exception as ex:
#         print(ex, file=stderr)
#         exit(1)

# if __name__ == '__main__':
#     print(flask.__version__)
#     main()