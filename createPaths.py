from pathlib import Path
import sys

print(sys.platform)
# In Linux, the path separator is /. In Windows, it is either \ or /. So just use forward slashes and you will be fine.

def createPaths(years):
    '''Create paths for required folders'''
    
    pD = Path('./'+years+'/data')
    try:
        pD.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(years+' already exists')

    pP = Path('./'+years+'/pics')
    try:
        pP.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(years+' already exists')

    pS = Path('./'+years+'/sites')
    try:
        pS.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print('sites already exists')

    pSTS = Path('./'+years+'/sites/ts')
    try:
        pSTS.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print('sites/ts already exists')

    return([pD,pP,pS,pSTS])
