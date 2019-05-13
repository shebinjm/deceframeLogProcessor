
from py2neo import Graph
from flask import Flask
from flask_socketio import SocketIO
import json
import socket
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


class JsonToNeo4j:
    def import_content(self, data):
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

        socketio.emit('my response', json)
        print('send message successfully')
        def messageReceived(methods=['GET', 'POST']):
            print('message was received!!!')

        @socketio.on('my event')
        def handle_my_custom_event(json, methods=['GET', 'POST']):
            print('received my event: ' + str(json))
            socketio.emit('my response', json, callback=messageReceived)


    def app1(self):
        print('Thread 1')
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('127.0.0.1', 8088))
        serverSocket.listen(5)  # become a server socket, maximum 5 connections
        connection, address = serverSocket.accept()

        buf = ''
        while True:
            data = connection.recv(1024)
            if len(data) > 0:
               buf += data.decode('utf-8')
               print(buf)
            else:
               break

        JsonToNeo4j().import_content(buf)


    def app2(self):
            print('Thread 2')
#            socketio.run(app, host='0.0.0.0')


if __name__ == '__main__':
        print('starting Thread 1')
#        t1 = threading.Thread(target=JsonToNeo4j().app1)
        socketio.run(app, host='0.0.0.0')
        print('starting Thread 2')
        t2 = threading.Thread(target=JsonToNeo4j().app2)
#        t1.start()
        t2.start()
