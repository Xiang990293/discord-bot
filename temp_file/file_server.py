#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler

HandlerClass = SimpleHTTPRequestHandler
ServerClass  = http.server.HTTPServer
Protocol     = "HTTP/1.0"
PORT		 = 1346
DIRECTORY    = "/temp_file"

# if sys.argv[1:]:
#     port = int(sys.argv[1])
# else:
#     port = PORT
# server_address = ('127.0.0.1', PORT)

# HandlerClass.protocol_version = Protocol
# httpd = ServerClass(server_address, HandlerClass)

# sa = httpd.socket.getsockname()
# print("Serving HTTP on", sa[0], "port", sa[1], "...")
# httpd.serve_forever()

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("::", PORT), Handler) as httpd:
	print("serving HTTP server at port", PORT)
	httpd.serve_forever()