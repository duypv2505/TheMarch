# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from TheMarch import app
from pymongo import MongoClient
from flask import session, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
import os
import simplejson
import json
from datetime import timedelta
from operator import itemgetter, attrgetter

import TheMarch.common as common

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['BANNER_IMAGE_FOLDER'] = 'dataset/banner/'
app.config['COFFEE_IMAGE_FOLDER'] = 'dataset/coffee/'
app.config['EVENT_IMAGE_FOLDER'] = 'dataset/event/'
app.config['BAND_IMAGE_FOLDER'] = 'dataset/band/'
app.config['GYM_IMAGE_FOLDER'] = 'dataset/gym/'
IGNORED_FILES = set(['.gitignore'])

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

result = common.current_db.User.find()
for item in result:
    print("Name: " + item["name"] + "email: " + str(item["email"]))

#############
# Object user
#############
class User(UserMixin):
    def __init__(self,id, user_name, password):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

#############
# Delare login form
#############
class LoginForm(FlaskForm):
    username = StringField('User Name'.decode('utf-8'),
                           validators=[InputRequired(), Length(min=4, max=80)], 
                           render_kw={"placeholder": "Tên đăng nhập".decode('utf-8')})
    password = PasswordField('Password'.decode('utf-8'),
                           validators=[InputRequired()], 
                           render_kw={"placeholder": "Mật khẩu".decode('utf-8')})
    remember = BooleanField('Ghi nhớ'.decode('utf-8'))

@app.route('/admin')
@login_required
def home_admin():
    """Renders the home page."""
    return render_template(
        'Admin/Coffee.html',
        title='Coffee admin page',
        year=datetime.now().year,
    )

#############
# Get detail of user
#############
@login_manager.user_loader
def load_user(user_id):
    current_user = common.current_db.User.find_one({"_id": ObjectId(user_id)})
    currentUser = User(user_id, current_user.get('username'), current_user.get('password'))
    return currentUser

#############
# Unauthorized user
#############
@login_manager.unauthorized_handler
def unauthorized():        
    return render_template('Admin/login.html', form = LoginForm())    
    #message = None
    #if common.reset_msg:
    #    message = common.reset_msg
    #    common.reset_msg = None
    #    return render_template('Admin/login.html', form = LoginForm(), reset_msg = message)
    #else:
    #    return render_template('Admin/login.html', form = LoginForm())

#############
#Login 
#############
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('Admin/login.html', form = LoginForm())

#############
#Login 
#############
@app.route('/login', methods=['POST'])
def do_admin_login():
    form = LoginForm(request.form)
    username = request.form["username"]
    password = request.form["password"]
    # CHeck username
    current_user = common.current_db.User.find_one({"email": username})
    if current_user:
        # Check pass
        #if check_password_hash(password, current_user.get('password')):
        #    return 'Login success'
        if password == current_user.get('password'):
            remember = request.form.get("remember", "no") == "yes"
            currentUser = User(current_user.get('_id'), username, password)
            # Excute Login
            if login_user(currentUser, remember=form.remember.data):
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=3000)
                session.update(dict(user=username))
                return redirect(url_for('home_admin'))   
            # Cannot Login
            else:                    
                return render_template('login.html', form=form, errorLogin = constants.ERR_LOGIN_FAILED.decode('utf-8'))
            # Check password failed
        else:                
            return render_template('login.html', form=form , passError= constants.ERR_PASSWORD.decode('utf-8'))
    # Check user name failed
    else:               
        return render_template('login.html', form=form, userError= constants.ERR_USER_NAME.decode('utf-8'))
    return render_template('login.html', form=form)
    
#############
# Upload banner
#############
@app.route("/upload_banner", methods=['POST'])
#@login_required
def upload_banner():    
    files = request.files['file']
    if files:          
        filename = secure_filename(files.filename)
        filename = common.gen_file_name(filename,app.config['BANNER_IMAGE_FOLDER'])   
        #banner_number = request.form['number']
        # save file to disk
        uploaded_file_path = os.path.join(app.config['BANNER_IMAGE_FOLDER'], filename)
        files.save(uploaded_file_path)
        # get file size after saving
        size = os.path.getsize(uploaded_file_path)
    return simplejson.dumps({"files_name": filename})

#############
# Banner controller
#############
@app.route("/banner", methods=['GET'])
#@login_required
def banner():    
    list_banner = load_banner_admin()
    return render_template(
        'Admin/banner.html',
        title='Banner manager page',
        banner_data = list_banner,
        year=datetime.now().year,
    )

def load_banner_admin():
    files = [f for f in os.listdir(app.config['BANNER_IMAGE_FOLDER']) if os.path.isfile(os.path.join(app.config['BANNER_IMAGE_FOLDER'],f)) and f not in IGNORED_FILES ]        
    file_display = []
    for f in files:        
        baner_url = os.path.join(app.config['BANNER_IMAGE_FOLDER'], f)
        banner_saved = common.banner_info(f, baner_url)             
        file_display.append(banner_saved)
    return file_display