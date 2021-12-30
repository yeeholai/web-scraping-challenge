from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def home():
	mars_dict = mongo.db.collection.find_one()
	return render_template("index.html", mars=mars_dict)


@app.route('/scrape')
def scrape():
	mars_data = scrape_mars.scrape()

	mongo.db.collection.update_many({}, {'$set': mars_data}, upsert=True)
	return redirect("/")

if __name__=="__main__":
	app.run(debug=True)