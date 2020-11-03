from flask import Flask, render_template, jsonify, redirect
import flask_pymongo 
import pymongo
from pymongo import MongoClient
# Import custom scraper
import scrape_mars
import bson
from bson.json_util import dumps


# Create an instance for Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_listings
collection = db.mars_data

# def dumps(obj):
#    try:
#        return obj.toJSON()
#    except:
#        return obj.__dict__
    
@app.route("/")
def index():
     # Store the entire team collection in a list
    #mars = list(collection.findAll())
    #@app.route('/users')
#def users():
#         user = db.mars_listings.db.find()
#         resp = dumps(user)
#         return resp
    
    mars_listings = collection.db.mars_listings.find()
    print(mars_listings)
    return render_template("index.html", mars_listings=mars_listings)


@app.route("/scrape")
def scraper():
    mars_listings = collection.db
    listings_data = scrape_mars.scrape()
    mars_listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
