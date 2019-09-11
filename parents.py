import pymongo
import json
import datetime
import smtplib, ssl

#db = pymongo.MongoClient("mongodb+srv://ninja:ninja@ninja-taedj.mongodb.net/admin?retryWrites=true&w=majority")["ninja"]
db = pymongo.MongoClient("localhost")["ninja"]

parent_home = {"lat":33.411182, "lon":-86.886951, "route":1, "email": "mpastorg@gmail.com"}

def lambda_handler(event,context):
    insert_parent(event['route'], event['lon'], event['lat'], event["email"])
    return "OK"


def insert_parent(route, lon, lat, email):
    myjson = {"location": {"type": "Point",
                           "coordinates": [lat, lon]},
              "route": route,
              "email": email
              }
    db.parents_poi.insert_one(myjson)


print(lambda_handler(parent_home, None))