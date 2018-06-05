"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from TheMarch import app
from pymongo import MongoClient

@app.route('/')
@app.route('/admin')
def home_admin():
    """Renders the home page."""
    return render_template(
        'Admin/master.html',
        title='Admin Page',
        year=datetime.now().year,
    )