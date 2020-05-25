def filter(client, projectName, fields, mongoQueries):
    cursor = client[projectName].find_many

