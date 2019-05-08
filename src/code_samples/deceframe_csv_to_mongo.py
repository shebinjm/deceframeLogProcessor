#!/usr/bin/env python
import sys,os
import pandas as pd
import pymongo
import json

class csv_to_mongo:
 def import_content(self,filepath):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['decframe']
    collection_name = 'perfmon'
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    print(data_json)
    db_cm.insert_many(data_json)



if __name__ == "__main__":
  filepath = 'perfmon.csv'
  csv_to_mongo().import_content(filepath)
