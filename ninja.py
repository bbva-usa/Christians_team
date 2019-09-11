import pymongo
import json
import datetime
import smtplib, ssl


event = {"lon":80, "lat":70, "route":1}

db = pymongo.MongoClient("mongodb+srv://ninja:ninja@ninja-taedj.mongodb.net/admin?retryWrites=true&w=majority")["ninja"]
#db = pymongo.MongoClient()


def handle(event):
    insert_position(event['route'], event['lon'], event['lat'])
    notifications = close_to(event['route'], event['lon'], event['lat'])
    send_emails(notifications)

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


def close_to(route, lon, lat):
    pipeline = [
        {
            "$geoNear": {
            "near": {"type": "Point", "coordinates": [lon, lat]},
            "key": "location",
            "maxDistance": 100000,
            "distanceField": "dist.calculated"
        }}
        ,{"$match": {"route": route}}

    ]
    mylist = list(db.parents_poi.aggregate(pipeline))
    if mylist[0]["dist"]["calculated"] < 1000:
        return mylist
    else:
        return None

def send_emails(mylist):
    for parent in mylist:
        email(parent["email"])


def email(email):
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("ninja.bbva.usa@gmail.com", "N1nj4bbv4")
        #server.login("mpastorg@gmail.com", "Astur14s")
        server.sendmail("ninja.bbva.usa@gmail.com", email, "Your bus is 5 minutes away")

print(handle(event))

#print(get_position("1"))

