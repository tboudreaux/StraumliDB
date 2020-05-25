from StraumliDB.mongo import utils, connect
from StraumliDB.projects import establishADB

if __name__ == "__main__":
    client = connect.connect_2_server('127.0.0.1')
    dbs = utils.list_db(client)
    if 'Astro' in dbs:
        utils.drop_db(client, 'Astro')
    establishADB.establish(client)

