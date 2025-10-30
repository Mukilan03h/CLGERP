import mongoengine
import os

def connect():
    MONGO_URI = os.environ.get('MONGO_URI')
    mongoengine.connect(host=MONGO_URI)
