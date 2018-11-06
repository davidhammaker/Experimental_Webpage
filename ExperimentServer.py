#!/usr/bin/env python
"""
This template may be used to construct a simple Python web server quickly and
efficiently.
"""
import os
import requests
import threading
from posts_db import get_posts
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, parse_qs
from socketserver import ThreadingMixIn
from socket import socket


index_file = "index.html"
posts_file = "posts.html"


def read_file(file_name, file_list):
    """Read files for HTTP transfer in response to GET requests"""
    try:
        file = open(file_name, "r")
        for item in file.readlines():
            file_list.append(item)
    except Exception:
        print("Could not read file.")
    finally:
        file.close()


def read_image(file_name):
    """Read image files for HTTP transfer in response to GET requests"""
    with open(file_name, 'rb') as file:
        return file.read()


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

        # Parse request
        req_name = unquote(self.path[1:])
        req_parse_list = req_name.split('.')
        print(req_name)
        if not req_name:
            print("SEND HTML")

        if not req_name:
            # Send '200 OK' with HTML:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            list_index = []
            read_file(index_file, list_index)
            final_index = (''.join(list_index))

            self.wfile.write(final_index.encode()) # The '' empty quotes should be replaced
                                      # with the HTML you want to send.

        elif req_parse_list[-1] == 'css':
            # Send '200 OK' with CSS:
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            list_index = []
            read_file(req_name, list_index)
            final_index = (''.join(list_index))

            self.wfile.write(final_index.encode())

        # PARTS THAT DON'T WORK YET
        elif req_parse_list[-1] == 'jpg':
            # Send '200 OK' with JPG:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()

            final_img = read_image(req_name)

            self.wfile.write(final_img)

        elif req_parse_list[-1] == 'html':
            # Send '200 OK' with HTML:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            list_index = []
            read_file(req_name, list_index)

            # Add posts to the HTML
            posts_raw = get_posts()  # These are obtained from posts_db
            print(posts_raw)
            # Figure out where to put the posts in the HTML
            insertion_index = 0
            for row in list_index:
                if "posts-bottom" in row:
                    insertion_index = list_index.index(row)
            for row in posts_raw:
                list_index.insert(insertion_index, '<p class="posts"><span class="date">' +
                                  '{date} - </span>{post}</p>'.format(date=row[0], post=row[1]))

            # Put the final HTML together and send it
            final_index = (''.join(list_index))
            self.wfile.write(final_index.encode())

        #PARTS I'M NOT USING:
        # # Send '303 Redirect':
        # self.send_response(303)
        # self.send_header('Location', 'uri/path')# 'uri/path' should be replaced
        #                                         # with the new URI for redirect.
        # self.end_headers()
        #
        # # Send '404 Not Found' with text:
        # self.send_response(404)
        # self.send_header('Content-type', 'text/plain; charset=utf-8')
        # self.end_headers()
        # self.wfile.write('404 - Page Not Found'.encode())
        #
        # # Send '400 Bad Request' with text:
        # self.send_response(400)
        # self.send_header('Content-type', 'text/plain; charset=utf-8')
        # self.end_headers()
        # self.wfile.write('400 - Bad Request'.encode())

    #NOT YET USING POST
    def do_POST(self):
        """Handle POST requests."""

        # Send '303 Redirect':
        self.send_response(303)
        self.send_header('Location', 'uri/path')# 'uri/path' should be replaced
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
    port = int(os.environ.get('PORT', 7000))
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    httpd.serve_forever()
