import os
import json
from GridboxConnector import GridboxConnector
import time

if __name__ == '__main__':
    print("test {}".format(os.environ))
    f = open('/share/cloudSettings.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    USER = os.getenv('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    f.close()
    data["login"]["username"] = USER
    data["login"]["password"] = PASSWORD

    while True:
        print(GridboxConnector(data).retrieve_live_data())
        time.sleep(60)