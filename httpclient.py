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
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        return 80

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        data_list = data.split("\r\n")
        code = data_list[0].split(" ")[1]
        return int(code)

    def get_headers(self,data):
        data_list = data.split("\r\n\r\n")
        header = data_list[0]
        return header

    def get_body(self, data):
        data_list = data.split("\r\n\r\n")
        body = data_list[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        url_components = urlparse(url)
        scheme = url_components.scheme
        hostname = url_components.hostname
        port = url_components.port
        path = url_components.path

        if(port == None):
            port = self.get_host_port(url)
        if(path == ""):
            path = "/"
        '''
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
        print(scheme)
        print(hostname)
        print(port)
        print(path)
        '''
        self.connect(hostname,port)

        request_payload = "GET {path} HTTP/1.1\r\n".format(path=path)
        request_payload += "Host: {host}:{port}\r\n\r\n".format(host=hostname,port=port)
        
        self.sendall(request_payload)
        data = self.recvall(self.socket)

        code = self.get_code(data)
        #header = self.get_headers(data)
        body = self.get_body(data)
        '''
        print("@@")
        print(data)
        print("@")
        print(code)
        print(body)
        print("@@")

        print('`````````````````')
        print(request_payload)
        print('`````````````````')
        '''
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        url_components = urlparse(url)
        scheme = url_components.scheme
        hostname = url_components.hostname
        port = url_components.port
        path = url_components.path
        '''
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
        print(scheme)
        print(hostname)
        print(port)
        print(path)
        '''
        content = ""
        try:
            for item in args.items():
                print(item)
                content += str(item[0]) + "=" + str(item[1]) + "&"
            content = content[:-1]
        except:
            pass

        self.connect(hostname,port)

        request_payload = "POST {path} HTTP/1.1\r\n".format(path=path)
        request_payload += "Host: {host}:{port}/\r\n".format(host=hostname,port=port,path=path)
        request_payload += "Content-Length: {length}\r\n\r\n".format(length=len(content))
        request_payload += content + "\r\n"

        self.sendall(request_payload)
        data = self.recvall(self.socket)
        '''
        print("@")
        print(data)
        print("@")
        '''
        code = self.get_code(data)
        #header = self.get_headers(data)
        body = self.get_body(data)
        '''
        print('`````````````````')
        print(path)
        print(request_payload)
        print(code)
        print(body)
        print('`````````````````')
        '''
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
