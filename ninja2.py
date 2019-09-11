import pymongo
import json
import datetime
import smtplib, ssl

#db = pymongo.MongoClient("mongodb+srv://ninja:ninja@ninja-taedj.mongodb.net/admin?retryWrites=true&w=majority")["ninja"]
db = pymongo.MongoClient("localhost")["ninja"]

def lambda_handler(event,context):
    try:
        myroute = event['route']
    except Exception:
        myroute = 1
    return get_position(myroute)


def insert_position(route, lon, lat):
    myjson = {"location": {"type": "Point",
                           "coordinates": [lat, lon]},
              "route": route,
              "dt": str(datetime.datetime.now())

              }
    db.routes_position.insert_one(myjson)


def get_position(route):
    cursor = db.routes_position.find_one({"route": route}, sort=[('dt', pymongo.DESCENDING)])
    return cursor

print(lambda_handler(None, None))