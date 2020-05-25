from StraumliDB.mongo import connect
from StraumliDB.projects import enroll

import os

Dataroot = "/mnt/p/d/Documents/Thomas/College/Summers/Summer2018/Chile2018/Data"
N1 = os.path.join(Dataroot, '20180516_N1')

if __name__ == "__main__":
    client = connect.connect_2_server('127.0.0.1')
    enroll.enroll_fits_directory(client.Astro, 'Test_Project', N1)
