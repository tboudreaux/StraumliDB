def filter(db, projectName, mongoQueries, fields=None, maping=None, pythonQuery=None):
    cursor = db[projectName].find(mongoQueries, fields)
    if maping:
        cursor = map(maping, cursor)
    if pythonQuery:
        cursor = filter(pythonQuery, cursor)
    return cursor

