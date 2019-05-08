
# mongo1.py

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# data base name : 'test-database-1'
mydb = client['decframe']
my_collection = mydb['logs']


import datetime

myrecord = {
        "author": "Teena",
        "title" : "PyMongo 103",
        "tags" : ["Freak", "Bingo", "Tutorial"],
        "date" : datetime.datetime.utcnow()
        }

record_id = mydb.logs.insert(myrecord)

print (record_id)
print (mydb.collection_names())
