#!/usr/bin/env python
import sys,os
import pandas as pd
import pymongo
from flask import Flask
import json
import socket

app = Flask(__name__)

class csv_to_mongo:
 def import_content(self,data):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['decframe']
    collection_name = 'perfmon'
    db_cm = mng_db[collection_name]
  #  cdir = os.path.dirname(__file__)
  #  file_res = os.path.join(cdir, filepath)

  #  data = pd.read_csv(file_res)
    data_json = json.loads(data)

    db_cm.remove()
    print(data_json)
    db_cm.insert_many(data_json)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', 8088))
serversocket.listen(5)  # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(64)
    if len(buf) > 0:
        csv_to_mongo().import_content(buf);
        break

if __name__ == "__main__":
  app.run()
