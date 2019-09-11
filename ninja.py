import pymongo
import json
import datetime
import smtplib, ssl


event = {"lat":33.399480, "lon":-86.890980, "route":1}
parent_home = {"lat":33.411182, "lon":-86.886951, "route":1}

db = pymongo.MongoClient("mongodb+srv://ninja:ninja@ninja-taedj.mongodb.net/admin?retryWrites=true&w=majority")["ninja"]
#db = pymongo.MongoClient()


def lambda_handler(event,context):
    insert_position(event['route'], event['lon'], event['lat'])
    notifications = close_to(event['route'], event['lon'], event['lat'])
    send_emails(notifications)

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


def close_to(route, lon, lat):
    pipeline = [
        {
            "$geoNear": {
            "near": {"type": "Point", "coordinates": [lat, lon]},
            "key": "location",
            "maxDistance": 10000,
            "distanceField": "dist.calculated"
        }}
        ,{"$match": {"route": route}}

    ]
    mylist = list(db.parents_poi.aggregate(pipeline))
    return mylist

def send_emails(mylist):
    for parent in mylist:
        dist = "{0:.2f}".format(parent["dist"]["calculated"])
        email(parent["email"], dist)


def email(email, distance):
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()
    msg = ("From: ninja.bbva.usa@gmail.com\r\nTo: %s\r\n\r\n" % email)
    msg = msg + "Subject: Bus position alert\r\n"+ "Your bus is " + distance + " meters away"

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("ninja.bbva.usa@gmail.com", "N1nj4bbv4")
        server.sendmail("ninja.bbva.usa@gmail.com", email, msg)

#print(handle(event))

#print(get_position("1"))

# https://forms.gle/F9a7jzMnJSyJpGzDA

# https://www.latlong.net

