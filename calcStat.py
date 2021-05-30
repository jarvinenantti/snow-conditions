import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from plotter import plotDecomposition


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


def deCompose(data,par,pS,rePlotDC):
    '''Decompose timeseries using statsmodels (additive model)'''
    
    # Loop add sites
    for site in data.keys():
        # Check that no missing periods
        if data[site].isna().any()[0]:
            print(site+' has NaN values after interpolation')
            continue
        # Decompose
        result_add = seasonal_decompose(data[site], model='additive', period=303, extrapolate_trend='freq')
        if rePlotDC:
            plotDecomposition(result_add,par,site,pS)
