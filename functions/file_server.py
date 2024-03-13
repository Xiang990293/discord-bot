#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler

HandlerClass = SimpleHTTPRequestHandler
ServerClass  = http.server.HTTPServer
Protocol	 = "HTTP/1.0"
PORT		 = 8081
DIRECTORY	= "/temp_file"

class FileServer(HandlerClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory="temp_file", **kwargs)
		
	def do_POST(self):
		if self.path == "/upload":
			ant = 1
			# Handle file upload logic here
			# Read the uploaded file data and save it
			# Respond with success or error message
		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(b"Endpoint not found")
		
		
if __name__ == "__main__":
	with socketserver.TCPServer(("0.0.0.0", PORT), FileServer) as httpd:
		print(f"serving HTTP server at minecraft-discord-bot.fly.dev:{PORT}")
		httpd.serve_forever()
