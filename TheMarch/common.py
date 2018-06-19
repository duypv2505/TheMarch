from pymongo import MongoClient

current_db = []

def connect_db():
    global current_db
    connection = MongoClient('ds016718.mlab.com', 16718)
    current_db = connection['themarch']
    current_db.authenticate('duypv', 'Pa$$w0rd1')    
    return current_db
