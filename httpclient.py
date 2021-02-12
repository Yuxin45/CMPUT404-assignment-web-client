#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):

    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
        # self.port
        

class HTTPClient(object):
    def __init__(self):
        self.port = 80
        self.path = ""
        # self.host
        
    #def get_host_port(self,url):

    def connect(self, host, port):
        """
        connect to socket 

        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):

        # return the http status code
        return int(data.split()[1])

    def get_headers(self,data):
        # return http headers
        spliter = "\r\n\r\n"
        # print(":header")
        # print(data.split(spliter)[0])
        # print("end header")
        return data.split(spliter)[0]

    def get_body(self, data):
        # return body
        spliter = "\r\n\r\n"
        # print("body")
        # print(data.split(spliter)[1])
        return data.split(spliter)[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket

    def recvall(self, sock):
        # return data received 
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    def parseURL(self,url):
        # parse url into port, host, and path
        url_data = urllib.parse.urlparse(url) # parse url data
        temp_port = url_data.port
        
        # print("port" + str(temp_port))
        self.host = url_data.hostname
        # print("hostname" + current_host)

        if temp_port != None:
            self.port = temp_port

        temp_path = url_data.path
        self.path = temp_path
        if temp_path == "":
            self.path = '/'

    def GET(self, url, args=None):
        # code = 500
        # body = ""

        self.parseURL(url)

        header = """GET {} HTTP/1.1\r\nHOST: {}\r\nConnection: close\r\n\r\n""".format(self.path, self.host)

        self.connect(self.host, self.port)
        self.sendall(header)
        data = self.recvall(self.socket)
        current_code = self.get_code(data)
        current_body = self.get_body(data)
        header = self.get_headers(data)
        # print("current code" + str(current_code))
        # print("current body"+current_body)
        print("begin of GET result ----------------")
        print(data)
        print("end of GET result ----------------")

        self.close()
        

        return HTTPResponse(current_code, current_body)

    def POST(self, url, args=None):
        # POST the given argument(args) into the give url argument
        # code = 50
        # 0
        body = ""
        body_len = 0

        self.parseURL(url)
        if args != None:
            # reference for urllib.parse.urlencode:  https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
            body = urllib.parse.urlencode(args)
            body_len = len(body)
        
        content = """POST {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-length: {}\r\n\r\n{}""".format(self.path, self.host, body_len, body)
        self.connect(self.host, self.port)
        self.sendall(content)
        data = self.recvall(self.socket)
        code = self.get_code(data)
        body = self.get_body(data)
        header = self.get_headers(data)
        print("begin of POST result ----------------")
        print(data)
        print("end of POST result ----------------")
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
