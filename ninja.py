import pymongo
import json
import datetime


event = {"lon":80, "lat":70, "route":1}

db = pymongo.MongoClient("mongodb+srv://ninja:ninja@ninja-taedj.mongodb.net/admin?retryWrites=true&w=majority")["ninja"]
db = pymongo.MongoClient()


def handle(event):
    insert_position(event['route'], event['lon'], event['lat'])
    cuantos = close_to(event['lon'], event['lat'])


def insert_position(route, lon, lat):
    myjson = {"location": {"type": "Point",
                  "coordinates": [lon, lat]},
     "route": route,
     "dt": str(datetime.datetime.now())

     }
    db.routes_position.insert_one(myjson)

def get_position(route):
    cursor = db.routes_position.find_one({"route": route}, sort=[('dt', pymongo.DESCENDING)])
    return cursor


def close_to(lon, lat):
    pipeline = [
        {
            "$geoNear": {
            "near": {"type": "Point", "coordinates": [lon, lat]},
            "key": "location",
            "maxDistance": 100000,
            "distanceField": "dist.calculated"
        }}
    , {
        "$sort": {
        "dt": -1
    }}
    , { "$limit": 1}
    ]
    mylist = list(db.routes_position.aggregate(pipeline))
    if mylist[0]["dist"]["calculated"] < 1000:
        return mylist[0]
    else:
        return None


print(handle(event))

#print(get_position("1"))

