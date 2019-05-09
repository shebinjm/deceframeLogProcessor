#!/usr/bin/env python

import socket

TCP_IP = 'localhost'
TCP_PORT = 8088
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
filename = 'cowrie.json'
f = open(filename, 'rb')
l = f.read(1024)
while (l):
    s.send(l)
    print('Sent ', repr(l))
    l = f.read(1024)
f.close()
print('Done sending')
#    s.send('Thank you for connecting')
s.close()
print('Successfully send the file')
