#!/usr/bin/python2
# Simple HTTP Server Expansion to transfer files with POST
# By Tuomo Kuure (tqre) (C)2020

import SimpleHTTPServer
import SocketServer
from sys import argv
import os

PORT = int(argv[1])

class ReqHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        # There was a reason for this zero here... lost it
        clen = int(self.headers.getheader('content-length', 0))
        req_path = self.path
        filename = req_path[1:]
        if not os.path.exists(filename[1:]):
            os.makedirs(filename[1:])
        body = self.rfile.read(clen)
        try:
            with open(filename[1:], 'w') as file:
                file.write(body)
                print "POST request body written to a file: " + filename[1:]
        except IOError:
            os.rmdir(filename[1:])
            with open(filename[1:], 'w') as file:
                file.write(body)
                print "POST request body written to a file: " + filename[1:]

reqhandler = ReqHandler
server = SocketServer.TCPServer(("", PORT), reqhandler)
print "Handling HTTP GET/HEAD/POST at port", PORT

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    exit()
