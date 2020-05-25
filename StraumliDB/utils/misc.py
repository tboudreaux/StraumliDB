import hashlib
import os

def hash_file(path, BLOCKSIZE=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def check_for_enrolled_file(db, projectName, path):
    assert os.path.exists(path)

    md5sum = hash_file(path)

    record = db[projectName].find_one({'md5sum': md5sum})
    return bool(record)
