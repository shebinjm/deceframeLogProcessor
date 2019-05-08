# mongo.py

from deceframe_csv_to_mongo import csv_to_mongo
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'decframe'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/decframe'

mongo = PyMongo(app)

@app.route('/perfmon', methods=['GET'])
def get_all_perfmon():

  perfmon = mongo.db.perfmon
  output = []
  for s in perfmon.find():
    s.pop('_id')
    output.append(s)

  return jsonify(output)


@app.route('/upload', methods=['POST'])
def upload_file():

# checking if the file is present or not.
 if 'file' not in request.files:
  return "No file found"

  file = request.files['file']
  file.save("test.csv")
  csv_to_mongo().import_content("test.csv");
  return "file successfully saved"


if __name__ == '__main__':
    app.run(debug=True)
