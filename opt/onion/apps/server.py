#!/usr/bin/env python

import time
import smbus
from urlparse import urlparse, parse_qs
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer

class OmegaCameraHandler(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        global bus
        global address
        self.address = 0x0a
        self.bus = smbus.SMBus(0)
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def set_angle(self, servo, angle):
        servo = int(servo)
        angle = int(angle)
        self.bus.write_byte_data(self.address, servo, angle)

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET (self):
        cmd = parse_qs(urlparse(self.path).query)
        print cmd
        self.set_angle(0, cmd['x'][0])
        self.set_angle(1, cmd['y'][0])
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    PORT = 8080
    Handler = OmegaCameraHandler
    server = SocketServer.TCPServer(('', PORT), Handler)

    print "serving at port", PORT
    server.serve_forever()
