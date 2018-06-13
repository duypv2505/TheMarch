from pymongo import MongoClient

def connect_db():
    connection = MongoClient('ds016718.mlab.com', 16718)
    db = connection['themarch']
    db.authenticate('duypv', 'Pa$$w0rd1')    
    return db
