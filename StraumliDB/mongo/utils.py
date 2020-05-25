def list_db(client):
    dbs = client.list_database_names()
    return dbs


def drop_db(client, dbName):
    cont = False
    dbs = list_db(client)

    if not dbName in dbs:
        raise KeyError('Database <{}> not enrolled in MongoDB Server'.format(dbName))

    while not cont:
        drop = input('Drop Database {}? [y/N]: '.format(dbName))
        drop = drop.upper()
        if drop == 'Y' or drop == 'N' or drop == '':
            cont = True
        else:
            print('Please enter either y or N')
    if drop == 'N' or drop == '':
        print('Dropping Database Cancelled')
    else:
        print('Dropping Database {}'.format(dbName))
        client.drop_database(dbName)

def create_db(client, dbName, schema):
    dbs = list_db(client)
    if dbName in dbs:
        raise KeyError('Database <{}> already enrolled in MongoDB Server'.format(dbName))
    assert isinstance(schema, dict)

    db = client[dbName]
    schemaTable = db['schema']

    schemaTable.insert(schema)
    return db

