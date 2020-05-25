from StraumliDB.utils import misc

import itertools
from astropy.io import fits
import os
import warnings

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
    else:
        print(f"Enrolling {path}")

    with fits.open(path) as hdul:
        header = hdul[0].header
    header = dict(header)
    header['filePath'] = path
    header['md5sum'] = misc.hash_file(path)
    header['COMMENT'] = str(header['COMMENT'])

    if '' in header:
        del(header[''])

    db[projectName].insert_one(header)

def enroll_fits_directory(db, projectName, path, recursive=False,
                          ignore_duplicates=True):
    isValidFits =  lambda x: x.endswith('.fits') and not x.startswith('.')

    fitsFiles = filter(isValidFits, os.listdir(path))
    fitsPaths = list(map(lambda x: os.path.join(path, x), fitsFiles))

    if recursive:
        for root, dirs, files in os.walk(path):
            subDirFiles = filter(isValidFits, files)
            subDirPaths = list(map(lambda x: os.path.join(root, x), subDirFiles))
            # fitsPaths = itertools.chain(fitsPaths, subDirPaths)
            fitsPaths.extend(subDirPaths)

    for fitsPath in fitsPaths:
        try:
            enroll_fits(db, projectName, fitsPath)
        except ValueError as e:
            if not ignore_duplicates:
                raise
            else:
               warnings.warn(
                       f'File {fitsPath} Already enrolled in Project, skipping',
                       Warning)
