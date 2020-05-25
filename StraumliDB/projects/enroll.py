from StraumliDB.utils import misc

import itertools
from astropy.io import fits
import os

def enroll_project(db, projectName, projectInfo):
    assert isinstance(projectInfo, dict)
    project = db[projectName]
    projects = db.schema.find_one()['Projects']
    db.schema.update_one(
       { "Projects": { '$gte': 0 } },
       {
         '$set': { "Projects": projects+1 }
       }
    )
    projectInfo['DefinedName'] = projectName
    if not bool(project.find_one({'DefinedName': projectName})):
        project.insert(projectInfo)
    else:
        print('Project Already Enrolled')
    return project

def enroll_fits(db, projectName, path):
    assert os.path.exists(path)
    if misc.check_for_enrolled_file(db, projectName, path):
        raise ValueError(f'File at {path} is already enrolled in project')

    with fits.open(path) as hdul:
        header = hdul[0].header
    header = dict(header)
    header['filePath'] = path
    header['md5sum'] = misc.hash_file(path)
    # print(header)
    for key in header:
        print(f"{key}: {header[key]}")
    del(header['COMMENT']) # TODO figure out why the comment field needs to be dropped
    db[projectName].insert_one(header)

def enroll_fits_directory(db, projectName, path, recursive=False,
                          ignore_duplicates=True):
    isValidFits =  lambda x: x.endswith('.fits') and not x.startswith('.')

    fitsFiles = filter(isValidFits, os.listdir(path))
    fitsPaths = map(lambda x: os.path.join(path, x), fitsFiles)

    if recursive:
        for root, dirs, files in os.path.walk(path):
            subDirFiles = filter(isValidFits, files)
            subDirPaths = map(lambda x: os.path.join(root, x), subDirFiles)
            fitsPaths.chain(fitsPaths, subDirPath)

    for fitsPath in fitsPaths:
        enroll_fits(db, projectName, fitsPath)
