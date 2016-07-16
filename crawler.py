# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 01:15:45 2016

@author: VuGoN
"""

import workerpool
import requests
import os
import sys

urls = []
#example
uri = "https://www.qwertee.com/images/designs/png/88589.png"

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getUri(id):
    urlHead = "https://cdn.qwertee.com/images/designs/png/"
    urlTail = ".png"
    return urlHead+str(id)+urlTail

def job(id):
    uri = getUri(id)
    res = requests.head(uri)
    if res.ok:
        #urls.appen(id)
        r = requests.get(uri)
        with open(str(id)+".png", "wb") as code:
            code.write(r.content)
        print 'downloaded: ',id
        

def pool(download_links):
    # Build our `map` parameters
    # Initialize a pool, 5 threads in this case
    pool = workerpool.WorkerPool(size=32)
    # The ``download`` method will be called with a line from the second 
    # parameter for each job.
    pool.map(job, download_links)
    # Send shutdown jobs to all threads, and wait until all the jobs have been completed
    pool.shutdown()
    pool.wait()


directory = 'image'
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)
params = sys.argv
if len(params)<3:
    print 'Please follow example:'
    print 'python crawler.py 1 10000'
if not isInt(params[1]) or not isInt(params[2]):
    print 'Incorect Input'

floor = int(params[1])
ceil = int(params[2])
download_links = [i for i in range(floor,ceil)]
print("Initialize a pool...")
pool(download_links)
print("end job...")