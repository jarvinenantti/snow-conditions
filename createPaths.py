from pathlib import Path


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

    return([pD,pP,pS])
