import pandas as pd

def interpolateNaNs(data):
    '''Linearly interpolate if values missing'''
    
    # Loop all sites
    for key in data.keys():
        data[key] = data[key].interpolate(method='spline', order=3)

    return(data)