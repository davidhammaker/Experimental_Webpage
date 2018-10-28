#!/usr/bin/env python
"""
This template may be used to construct a simple Python web server quickly and
efficiently.
"""
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
# from urllib.parse import unquote, parse_qs
from socketserver import ThreadingMixIn


class RequestHandler(BaseHTTPRequestHandler):
    """
    This is the request handler, inheriting from
    http.server.BaseHTTPRequestHandler. It contains templates for functions that
    handle GET and POST requests.

    Methods:
        do_GET(self): Handle GET requests.

        do_POST(self): Handle POST requests.
    """
    def do_GET(self):
        """Handle GET requests."""

        # Send '200 OK' with HTML:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(''.encode()) # The '' empty quotes should be replaced with
                                      # the HTML you want to send.

        # Send '303 Redirect':
        self.send_response(303)
        self.send_header('Location', 'uri/path') # 'uri/path' should be replaced
                                                 # with the new URI for redirect.
        self.end_headers()

        # Send '404 Not Found' with text:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('404 - Page Not Found'.encode())

        # Send '400 Bad Request' with text:
        self.send_response(400)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('400 - Bad Request'.encode())

    def do_POST(self):
        """Handle POST requests."""

        # Send '303 Redirect':
        self.send_response(303)
        self.send_header('Location', 'uri/path')  # 'uri/path' should be replaced
                                                  # with the new URI for redirect.
        self.end_headers()

        # Send '404 Not Found' with text:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('404 - Page Not Found'.encode())

        # Send '400 Bad Request' with text:
        self.send_response(400)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('400 - Bad Request'.encode())

        # Refresh page with '303 Redirect':
        self.send_response(303)
        self.send_header('Location', '/')  # '/' redirects to the same page.
        # with the new URI for redirect.
        self.end_headers()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    httpd.serve_forever()