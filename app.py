import json
from flask import Flask, request, jsonify
import pymongo
import dns
from datetime import datetime

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://aniket:mongodb@cluster0.gosrh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = client["mydatabase"]
mycol = mydb["taskCollection"]

@app.route('/', methods=['GET'])
def notvalid():
    return "This Route is Not Available!"

@app.route('/view', methods=['GET'])
def query_records():
    alldata = mycol.find()
    df = []
    for x in alldata:
        df.append(x)
    return jsonify(df)

@app.route('/create', methods=['POST'])
def create_record():
    record = request.form
    defaultDict = {}
    defaultDict['date'] = record['date']
    defaultDict['startTime'] = record['startTime']
    defaultDict['endTime'] = record['endTime']
    startTime = "{} {}".format(defaultDict['date'],defaultDict['startTime'])
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")  
    endTime = "{} {}".format(defaultDict['date'],defaultDict['endTime'])
    endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")  
    dailyHoursCount = endTime - startTime
    defaultDict['dailyHoursCount'] = str(dailyHoursCount)
    print(defaultDict)
    x = mycol.insert_one(defaultDict)
    return "Record Inserted"

@app.route('/update', methods=['PUT'])
def update_record():
    record = request.form
    mydict = mycol.find_one()
    defaultDict = {}
    defaultDict['date'] = record['date']
    defaultDict['startTime'] = record['startTime']
    defaultDict['endTime'] = record['endTime']
    defaultDict['dailyHoursCount'] = record['dailyHoursCount']
    newvalues = {"$set": defaultDict}
    mycol.update_one(mydict, newvalues)
    return "Record Updated"

@app.route('/delete', methods=['DELETE'])
def delete_record():
    record = request.form
    defaultDict = {}
    defaultDict['date'] = record['date']
    defaultDict['startTime'] = record['startTime']
    defaultDict['endTime'] = record['endTime']
    defaultDict['dailyHoursCount'] = record['dailyHoursCount']
    mycol.delete_one(defaultDict)
    return "Record Deleted"

if __name__ == "__main__":
    app.run(debug=True)
