import pandas as pd
import numpy as np
from pathlib import Path
import datetime as dt


def fillMaster(master,startWinter):
    '''Fill master dataframe with sites with year columns'''
    
    # Years as columns
    p = Path('./data')
    winter = startWinter

    # Iterate every file from the data-folder
    for year in list(p.glob('**/*.pkl')):
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