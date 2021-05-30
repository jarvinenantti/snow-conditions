from pathlib import Path
import datetime as dt
import pandas as pd


def createTimeseries(sites,pD):
    '''Transform yearly data into timeseries format per site'''
    
    # Initialize dictionary with empty dataframes
    ts= {}
    for site in sites:
        ts[site] = pd.DataFrame()
    
    # Iterate every file from the data-folder (sort by name)
    p = Path('./'+str(pD))
    for year in list(sorted(p.glob('**/*.pkl'))):
        unpickled_df = pd.read_pickle(year)
        # Iterate every site inside the year-file
        for (site, data) in unpickled_df.iteritems():
            if site == 'unit':
                continue
            dfS = pd.DataFrame(data = data) # single site, single period
            # Append data to site dataframe
            if ts[site].empty:
                ts[site] = dfS
            else:
                ts[site] = ts[site].append(dfS)
        
    return(ts)
