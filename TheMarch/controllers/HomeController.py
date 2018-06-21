"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory
from TheMarch import app
from pymongo import MongoClient
import TheMarch.common as common
import os
import simplejson
import json
from datetime import timedelta
from operator import itemgetter, attrgetter

#db = common.connect_db()
#result = db.User.find()
#for item in result:
#    print("Name: " + item["name"] + "email: " + str(item["email"]))
IGNORED_FILES = set(['.gitignore'])

@app.route('/')
@app.route('/home')
def home():
    list_banner = load_banner()
    """Renders the home page."""
    return render_template(
        'Home/home.html',
        title='Home Page',
        banner = list_banner,
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

#############
# Load banner
#############
@app.route("/load_banner", methods=['POST'])
def load_banner():
    files = [f for f in os.listdir(app.config['BANNER_IMAGE_FOLDER']) if os.path.isfile(os.path.join(app.config['BANNER_IMAGE_FOLDER'],f)) and f not in IGNORED_FILES ]        
    file_display = []
    for f in files:        
        baner_url = os.path.join(app.config['BANNER_IMAGE_FOLDER'], f)
        banner_saved = common.banner_info(f, baner_url)             
        file_display.append(banner_saved)
    #Sort by productType
    #file_display.sort(key=itemgetter('name'))
    #return json.dumps([ob.__dict__ for ob in file_display])
    return file_display

@app.route('/load_banner_image/<path:filename>')
def load_banner_image(filename):
    return send_from_directory(app.config['BANNER_IMAGE_FOLDER'], filename=filename)