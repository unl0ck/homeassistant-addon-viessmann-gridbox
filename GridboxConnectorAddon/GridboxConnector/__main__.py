import os
import json
from GridboxConnector import GridboxConnector

if __name__ == '__main__':
    print(os.environ)
    f = open('/data/cloudSettings.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    GridboxConnector(data).retrieve_live_data()