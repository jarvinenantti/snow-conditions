import pandas as pd

def interpolateNaNs(data):
    '''Linearly interpolate if missing values'''
    
    # Loop all sites
    for key in data.keys():
        data[key] = data[key].interpolate()

    return(data)