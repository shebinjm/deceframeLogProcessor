import json
from py2neo import Graph

#authenticate("localhost:7474", "neo4j", "neo4j")
#graph = Graph()
url = "http://localhost:7474"
user = "neo4j"
pwd = "neo4j"

#graph = Graph(url, auth=(user, pwd),bolt=True, secure=True, http_port = 24789, https_port = 24780)
graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="admin123")

with open('src/cowrie.json') as data_file:
    json = json.load(data_file)

query = """
WITH {json} AS document
UNWIND document.events AS event
MERGE (m:machine{ip:event.src_ip,sensor:event.sensor})
MERGE (c:DecEvent {event:event.eventid,timestamp:event.timestamp,sensor:event.sensor})
MERGE (m)-[:occured]->(c)
"""

print(graph.run(query, json=json))
