
from app import app
from config import client
from bson.json_util import dumps
import random
import string
from flask import Flask, jsonify, request, make_response


db = client.Bank
col = db.Account

@app.route("/api/createuser",methods=['POST'])
def createUser():
    try:
        record = request.get_json()
        id = record.get("_id")
        filter = {"_id": id}
        accno = ''.join(random.choices(string.digits, k=8))
        col.insert_one(record)
        col.update_one(filter, {"$set":{"AccountNo ":accno}})
        res = make_response(jsonify({"Message": "Record inserted", "Account Number": accno}), 200)
        return res
    except:
        res = {
            "Message":"Error occurred !"
        }
        return make_response(jsonify(res),503)

@app.route("/api/users", methods=['GET'])
def getUsers():
    try:
        users = col.find()
        res = dumps(users)
        return res
    except:
        res = {
            "Message": "Error occurred !"
        }
        return make_response(jsonify(res), 503)

@app.route("/api/users/<accno>", methods=['GET'])
def getSingleUser(accno):
    try:
        user = col.find_one({"AccountNo ":accno})
        if user:
            res = {
                "Account Info": user
            }
            return make_response(jsonify(res), 200)
        else:
            res = {
                "Message": "Account not found!"
            }
            return make_response(jsonify(res), 404)
    except:
        res = {
            "Message": "Error occurred !"
        }
        return make_response(jsonify(res), 503)

@app.route("/api/update/<accno>", methods=['PUT'])
def updateUser(accno):
    try:
        if col.find_one({"AccountNo ":accno}):
            req = request.get_json()
            print(req)
            filter = {"AccountNo ":accno}
            for i in req:
                col.update_one(filter, {"$set":{i:req[i]}})
            return "Record updated successfully!",200
        else:
            res = {
                "Message":"Account not found!"
            }
            return make_response(jsonify(res), 404)
    except:
        res = {
            "Message": "Error occurred !"
        }
        return make_response(jsonify(res), 503)


@app.route("/api/delete/<accno>", methods=["DELETE"])
def delete_collection(accno):
    try:
        if col.find_one({"AccountNo ":accno}):
            query = {"AccountNo ":accno}
            col.delete_one(query)
            res = make_response(jsonify({"Message": "Record deleted successfully"}), 200)
            return res
        else:
            res = {
                "Message": "Account not found!"
            }
            return make_response(jsonify(res), 404)
    except:
        res = {
            "Message": "Error occurred !"
        }
        return make_response(jsonify(res), 503)


