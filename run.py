import os, sys
import boto3
import datetime
import json
import time
from base64 import b64encode

from config import *
WAIT_TIME = 60
MONITOR_TIME = 60


#################################
# AUXILIARY FUNCTIONS
#################################
def get_aws_credentials(AWS_PROFILE):
    session = boto3.Session(profile_name=AWS_PROFILE)
    credentials = session.get_credentials()
    return credentials.access_key, credentials.secret_key


def loadConfig(configFile):
    data = None
    with open(configFile, 'r') as conf:
        data = json.load(conf)
    return data


#################################
# SERVICE 1: SETUP
#################################
def setup():
    print('setup')


#################################
# SERVICE 2: SUBMIT JOB
#################################
def submitJob():
    if len(sys.argv) < 3:
        print('Use: run.py submitJob jobfile')
        sys.exit()

    # Step 1: Read the job configuration file
    jobInfo = loadConfig(sys.argv[2])
    print('submit job')


#################################
# SERVICE 3: START CLUSTER
#################################
def startCluster():
    if len(sys.argv) < 3:
        print('Use: run.py startCluster configFile')
        sys.exit()

    thistime = datetime.datetime.now().replace(microsecond=0)
    #Step 1: set up the configuration files
    s3client = boto3.client('s3')
    print('start cluster')


#################################
# SERVICE 4: MONITOR JOB
#################################

def monitor(cheapest=False):
    if len(sys.argv) < 3:
        print('Use: run.py monitor spotFleetIdFile')
        sys.exit()

    if '.json' not in sys.argv[2]:
        print('Use: run.py monitor spotFleetIdFile')
        sys.exit()

    if len(sys.argv) == 4:
        cheapest = sys.argv[3]

    print('monitor')

#################################
# MAIN USER INTERACTION
#################################
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Use: run.py setup | submitJob | startCluster | monitor')
        sys.exit()

    if sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'submitJob':
        submitJob()
    elif sys.argv[1] == 'startCluster':
        startCluster()
    elif sys.argv[1] == 'monitor':
        monitor()
