from pathlib import Path
import datetime as dt
import numpy as np
import pandas as pd


def returnMaster(sites,startWinter,pD):
    '''Return master dataframe with sites with year columns'''
    
    # To calculate statistics for each site
    # create general DatetimeIndex column (no leap year)
    rng = pd.date_range(pd.Timestamp("2000-09-01"),
                        periods=303, freq='d')
    gI = rng.strftime('%m-%d')
    days = np.linspace(1, 303, 303, dtype=int)

    # Create one master dictionary of sites
    master = {}
    for c in sites:
        master[c] = pd.DataFrame(index=gI)
        master[c]['date'] = master[c].index
        master[c].index = days
    
    # Years as columns
    p = Path('./'+str(pD))
    winter = startWinter

    # Iterate every file from the data-folder (sort by name)
    for year in list(sorted(p.glob('**/*.pkl'))):
        unpickled_df = pd.read_pickle(year)
        # Convert datetime index to string and remove year
        unpickled_df.index = unpickled_df.index.strftime('%m-%d')
        # Iterate every site
        for (site, data) in unpickled_df.iteritems():
            if site == 'unit':
                continue
            dfS = pd.DataFrame(data = data) # single site, single period
            # Set winter for column name
            name = str(winter)+'-'+str(winter+1)
            dfS = dfS.rename(columns={site: name})
            # Create new "date"-column from index
            dfS['date'] = dfS.index
            # Drop duplicates
            dfSD = dfS.drop_duplicates(subset="date")
            l = len(dfSD)
            # Set integer list of days as index
            dfSD.index = np.linspace(1, l, l, dtype=int)
            # Join based on date-column (to restrict sort)
            master[site] = master[site].merge(dfSD, how='left',
                                                  left_on='date', right_on='date')
        
        winter += 1
    
    return(master)


'''
# To test
year = list(p.glob('**/*.pkl'))[0]
unpickled_df = pd.read_pickle(year)
unpickled_df.index = unpickled_df.index.strftime('%m-%d')
center = 'Inari Saariselkä matkailukeskus'
data = unpickled_df[center]
dfS = pd.DataFrame(data = data) # single site, single period
name = str(winter)+'-'+str(winter+1)
dfS = dfS.rename(columns={center: name})
dfS['date'] = dfS.index
dfSD = dfS.drop_duplicates(subset="date")
l = len(dfSD)
dfSD.index = np.linspace(1, l, l, dtype=int)
test = master[center]
test = test.merge(dfSD, how='left', left_on='date', right_on='date')
winter += 1
year = list(p.glob('**/*.pkl'))[1]
test2 = test.merge(dfSD, how='left', left_on='date', right_on='date')
'''