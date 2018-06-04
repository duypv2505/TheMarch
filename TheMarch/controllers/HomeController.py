"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from TheMarch import app
from pymongo import MongoClient

connection = MongoClient('ds016718.mlab.com', 16718)
db = connection['themarch']
db.authenticate('duypv', 'Pa$$w0rd1')
result = db.User.find()
for item in result:
    print("Name: " + item["name"] + "email: " + str(item["email"]))

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
