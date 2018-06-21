from pymongo import MongoClient
import os
from TheMarch import app

current_db = []
IGNORED_FILES = set(['.gitignore'])

class banner_info:
  def __init__(self,name , url):
    self.name = name
    self.url = url

def connect_db():
    global current_db
    connection = MongoClient('ds016718.mlab.com', 16718)
    current_db = connection['themarch']
    current_db.authenticate('duypv', 'Pa$$w0rd1')    
    return current_db

#############
# Generate valid name of image file
#############
def gen_file_name(filename, path):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(path, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename

def load_banner_image():
    files = [f for f in os.listdir('TheMarch/' + app.config['BANNER_IMAGE_FOLDER']) if os.path.isfile(os.path.join('TheMarch/' + app.config['BANNER_IMAGE_FOLDER'],f)) and f not in IGNORED_FILES ]        
    file_display = []
    for f in files:        
        #baner_url = os.path.join(app.config['BANNER_IMAGE_FOLDER'], f)
        baner_url = "load_banner_image/%s" % f
        banner_saved = banner_info(f, baner_url)             
        file_display.append(banner_saved)
    return file_display