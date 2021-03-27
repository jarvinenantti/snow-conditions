import pandas as pd

def calcRowStat(data):
    '''Calculate statistics columns'''
    # mean, 50% and 80% quartiles
    
    # Loop all sites
    for key in data.keys():
        # Calculate statistics for each day (row) for all years
        mean = data[key].mean(axis=1, numeric_only=True)
        q10 = data[key].quantile(q=0.1, axis=1, numeric_only=True, interpolation='linear')
        q25 = data[key].quantile(q=0.25, axis=1, numeric_only=True, interpolation='linear')
        q75 = data[key].quantile(q=0.75, axis=1, numeric_only=True, interpolation='linear')
        q90 = data[key].quantile(q=0.9, axis=1, numeric_only=True, interpolation='linear')

        # Add as rows
        data[key]['mean'] = mean
        data[key]['q10'] = q10
        data[key]['q25'] = q25
        data[key]['q75'] = q75
        data[key]['q90'] = q90

    return(data)


def calcYearStat(data,site,year):
    '''Calculate key statistical values per site per year'''

    # Loop all sites
    for site in data.keys():
        for year in site.keys():
            # Pandas describe key statistics
            year.describe()