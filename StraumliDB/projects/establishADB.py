from StraumliDB.mongo import connect
from StraumliDB.mongo import utils

def establish(client, dbName='Astro'):
    dbs = utils.list_db(client)

    if dbName in dbs:
        print('Database <{}> already exists in Database'.format(dbName))
        utils.drop_db(client, dbName)
    utils.create_db(client, dbName, {'Projects':0})
