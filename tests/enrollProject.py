from StraumliDB.mongo import connect
from StraumliDB.projects import enroll
from StraumliDB.utils import misc



if __name__ == "__main__":
    client = connect.connect_2_server('127.0.0.1')

    enroll.enroll_project(
            client['Astro'],
            'Test_Project',
            {
                'Project Name': "Test_Project",
                'Principal Investigator': "Thomas Boudreaux",
                'Institution': "Dartmouth College"
            })

    # Validate Entry
    entry = {
            'Project Name': "Test_Project",
            'Principal Investigator': "Thomas Boudreaux",
            'Institution': "Dartmouth College"
            }
    result = client.Astro.Test_Project.find_one()
    testResults = map(
            lambda x: result[x] == entry[x],
            entry)

    print(any(testResults))
