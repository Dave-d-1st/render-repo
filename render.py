from flask import Flask,request
from tinydb import TinyDB, Query
from fastapi import FastAPI
import json

tinydb = TinyDB("db.json")
app=FastAPI()

allow_new_users = False

@app.post('/',responses={200:{"":""},404:{"Balls",""}})
def register():
    data: str = request.json
    query = Query()
    if not tinydb.contains(query.name==data['name']):
        tinydb.insert(data)
    return "",200
@app.get('/')
def get_user():
    name = request.args.get("name")
    deviceName = request.args.get("device name")
    product = request.args.get("product")
    id = request.args.get("id")
    query = Query()
    auth = tinydb.contains(query.name==name and query.deviceName == deviceName and query.product == product and query.id == id)
    print(auth)
    if not auth:
        return "",200
    else:
        return "",403

@app.get('/database')
def database():
    return tinydb.all(),200


if __name__=="__main__":
    app.run(debug=True,port=35586,host="192.168.1.137")