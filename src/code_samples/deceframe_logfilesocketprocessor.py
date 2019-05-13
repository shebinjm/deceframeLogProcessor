from py2neo import Graph
import json
import socket
from flask import Flask
import threading

app = Flask(__name__)


def import_content(data):
    print('calling import content function......')
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="admin123")

    #        with open('src/cowrie.json') as data_file:
    #        data_json = json.load(data_file)
    data_json = json.loads(data)

    query = """
    WITH {json} AS document
    UNWIND document.events AS event
    MERGE (m:machine{ip:event.src_ip,sensor:event.sensor})
    MERGE (c:DecEvent {event:event.eventid,timestamp:event.timestamp,sensor:event.sensor})
    MERGE (m)-[:occured]->(c)
    """
    print(graph.run(query, json=data_json))

    #        socketio.emit('my response', json)
    print('send message successfully')
    graph.close()


def app1():

    print('Thread 1')
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', 8088))
    serverSocket.listen(5)  # become a server socket, maximum 5 connections

    while True:
        print("Waiting for connection");
        connection, address = serverSocket.accept()
        buf = ''
        while True:
            print("listening....");
            try:
                data = connection.recv(1024)
                if len(data) > 0:
                    buf += data.decode('utf-8')
                    print(buf)
                else:
                    print("calling else")

            except:
                print(buf)
 #               import_content(buf)
                print("Socket connection closed")
                connection.close()
                break



if __name__ == '__main__':
    print("activate job");
    t1 = threading.Thread(target=app1)
    t1.start()
    app.run(threaded=True)
    t1.join()
