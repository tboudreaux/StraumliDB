from pymongo import MongoClient

def connect_2_server(uri):
    client=MongoClient('127.0.0.1')
    return client
