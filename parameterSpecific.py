import pandas as pd

def parameterSpecific(data,par):
    '''Do (if) parameter specific tricks'''
    
    # Loop all sites
    for key in data.keys():
        
        # If snow, replace all -1 with 0
        if par == 'snow_aws':
            data[key] = data[key].replace(-1, 0)

    return(data)