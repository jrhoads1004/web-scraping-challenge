from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
    #Save data into a listing
    mars_data=mongo.db.mars_data.find_one()

    #Render results into html
    return render_template("index.html", mars_data=mars_data)

@app.route("/scraper")
def scraper():
    #call function scrape from scrape_mars.py file
    mars_results = scrape_mars.scrape()

    #create mars_data collection into mars_db
    mars_data = mongo.db.mars_data

    #Update results (insert or append if existing)
    mars_data.update({},mars_results, upsert=True)

    #return back to home
    return redirect("/", code=302)

if __name__=="__main__":
    app.run(debug=True)
