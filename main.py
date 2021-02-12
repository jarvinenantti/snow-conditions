# coding=utf-8

# Fetch FMI open data using "fmiopendata"-library
# https://github.com/pnuu/fmiopendata
# pip install fmiopendata
# numpy, requests, pandas, datetime, math, matplotlib

from toPandasDF import toPandasDF
from fetchFmiData import fetchFmiData
from splitWinters import splitWinters
from plotter import plotYear, plotSite
from interpolateNaNs import interpolateNaNs
from calcStat import calcStat
from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Ski Centers: Saariselkä, Levi, Ylläs/Pallas/Ollos, Pyhä/Luosto, Ruka, Syöte, Vuokatti, Kilpisjärvi
skiCenters = ['Saariselkä','Levi','Ylläs|Pallas|Ollos','Pyhä|Luosto','Ruka','Syöte','Vuokatti','Kilpisjärvi']
# And closest FMI-sites with snow records
sites = ['Inari Saariselkä matkailukeskus','Kittilä kirkonkylä','Kittilä Kenttärova','Kemijärvi lentokenttä','Kuusamo Kiutaköngäs','Taivalkoski kirkonkylä','Sotkamo Kuolaniemi','Enontekiö Kilpisjärvi kyläkeskus']
siteToSki = dict(zip(sites, skiCenters))

# Define timeperiod in winters
startWinter = 2010
endWinter = 2020 # Currently 2020 max
assert endWinter > startWinter

# Generate timeperiods for winters
[startTimes,endTimes] = splitWinters(startWinter,endWinter)

# Example timeperiod
# startTime = '2020-09-01T00:00:00'
# endTime = '2021-06-30T00:00:00'

# Define parameter of interest
par = 'snow_aws' # snow cover

# Fetch, transform and save year-by-year data and pics
for startTime,endTime in zip(startTimes,endTimes):
    
    # Create unique name for yearly parameter query
    name = par+'_'+startTime+'_'+endTime
    # If pickle-file exists, skip
    if Path('./data/'+name+'.pkl').is_file():
        print(name+' already exists')
        continue
    # Fetch data as a list of queries
    fmiData = fetchFmiData(sites,startTime,endTime)
    # Cumulate all records of parameter into a single pandas dataframe
    df = toPandasDF(fmiData,sites)
    # Save to pickle-files (data-folder)
    df.to_pickle("./data/"+name+".pkl")
    # Save yearly plots (pics-folder)
    plotYear(df,skiCenters,par,name)

# To calculate statistics for each site

# Create general DatetimeIndex column (ei karkausvuotta)
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

# with dataframe of years as columns
p = Path('./data')
winter = startWinter

# Iterate every file from the data-folder
for year in list(p.glob('**/*.pkl')):
    unpickled_df = pd.read_pickle(year)
    # Convert datetime index to string and remove year
    unpickled_df.index = unpickled_df.index.strftime('%m-%d')
    # Iterate every site
    for (center, data) in unpickled_df.iteritems():
        if center == 'unit':
            continue
        dfS = pd.DataFrame(data = data) # single site, single period
        # Set winter for column name
        name = str(winter)+'-'+str(winter+1)
        dfS = dfS.rename(columns={center: name})
        # Create new "date"-column from index
        dfS['date'] = dfS.index
        # Drop duplicates
        dfSD = dfS.drop_duplicates(subset="date")
        l = len(dfSD)
        # Set integer list of days as index
        dfSD.index = np.linspace(1, l, l, dtype=int)
        # Join based on date-column (to restrict sort)
#         master[center] = master[center].join(dfS, how='left', sort=False)
        master[center] = master[center].merge(dfSD, how='left',
                                              left_on='date', right_on='date')
        
    winter += 1

# Fill NaN values with linear interpolation
master = interpolateNaNs(master)

# Calculate statistics columns
master = calcStat(master)

# Plot site specific statistics
plotSite(master,par,startWinter,endWinter,siteToSki)

# print(type(fmiData))
# print(fmiData)
# print(fmiData[0].data[sites[0]]['snow_aws'])

# print(df)
# cols = list(df.columns.values)
# print(cols)
# print(df.index)
# for ind in df.index:
#     print(ind)

# unpickled_df = pd.read_pickle("./dummy.pkl")


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