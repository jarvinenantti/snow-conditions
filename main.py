# coding=utf-8

'''
Fetch FMI open data using "fmiopendata"-library
https://github.com/pnuu/fmiopendata
pip install fmiopendata
numpy, requests, pandas, datetime, math, matplotlib, pathlib, os

Configured for 1.9. - 30.6. (~winter) !
'''

from splitWinters import splitWinters
from checkAvailability import checkAvailability
from fetchFmiData import fetchFmiData
from toPandasDF import toPandasDF
from plotter import plotYear, plotSite
from fillMaster import fillMaster
from parameterSpecific import parameterSpecific
from interpolateNaNs import interpolateNaNs
from calcStat import calcRowStat, calcYearStat

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Re-plot ?
rePlotYears = False
rePlotSites = False

# Ski Centers: Saariselkä, Levi, Ylläs/Pallas/Ollos, Pyhä/Luosto, Ruka, Syöte, Vuokatti, Kilpisjärvi
skiCenters = ['Saariselkä','Levi','Ylläs|Pallas|Ollos','Pyhä|Luosto','Ruka','Syöte','Vuokatti','Kilpisjärvi']

# And closest FMI-sites with snow records
sites = ['Inari Saariselkä matkailukeskus','Kittilä kirkonkylä','Kittilä Kenttärova','Kemijärvi lentokenttä','Kuusamo Kiutaköngäs','Taivalkoski kirkonkylä','Sotkamo Kuolaniemi','Enontekiö Kilpisjärvi kyläkeskus']

# Establishment year / snow record availability of the FMI site
# Sotkamo 1989->2009
# Enontekiö 1951->1979
est = [1976, 2009, 2002, 2006, 1966, 2002, 2009, 1979]
excl = [[1976], [2009], [2002], [0], [1967], [2002], [0], [1982]] # years to exclude

# Example query timeperiod (for past winters)
# startTime = '2020-09-01T00:00:00'
# endTime = '2021-06-30T00:00:00'
# Example query timeperiod (for ongoing winter)
# startTime = '2020-09-01T00:00:00'
# endTime = '2021-02-20T00:00:00'

# Define timeperiod in winters
startWinter = 1966
endWinter = 2020
assert endWinter > startWinter
years = str(startWinter)+'-'+str(endWinter)

# Define start and end of winter
startDay = '-09-01T00:00:00'
endDay = '-06-30T00:00:00'

# Generate data, pics, and sites folders
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
pS = Path('./'+'sites')
try:
    pS.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    print('sites already exists')

# Generate timeperiods for winters
[startTimes,endTimes] = splitWinters(startWinter,endWinter,startDay,endDay)

# Define parameter of interest
par = 'snow_aws' # snow cover

# Zip to dictionaries
siteToSki = dict(zip(sites, skiCenters))
siteToEst = dict(zip(sites, est))

# Fetch, transform and save year-by-year data and pics
for startTime,endTime in zip(startTimes,endTimes):

    # Choose sites based on data availability
    [avl_skiCenters,avl_sites] = checkAvailability(skiCenters,sites,startTime,endTime,est,excl)
    # Check if list is empty
    if not avl_sites:
        print("Empty year "+startTime[0:4]+"-"+endTime[0:4])
        continue
    else:
        print(startTime[0:4]+"-"+endTime[0:4])
        print(avl_sites)
    # Create unique name for yearly parameter query
    name = par+'_'+startTime+'_'+endTime

    # If pickle-file exists, skip fetch and save, but recreate plots
    if Path('./'+str(pD)+'/'+name+'.pkl').is_file():
        print(name+' already exists')
        if rePlotYears:
            df = pd.read_pickle(Path('./'+str(pD)+'/'+name+'.pkl'))
            plotYear(df,avl_skiCenters,par,name)
        continue

    # Fetch data as a list of queries
    fmiData = fetchFmiData(avl_sites,startTime,endTime)
    # Cumulate all records of parameter into a single pandas dataframe
    df = toPandasDF(fmiData,avl_sites)
    # Save to pickle-files (years/data-folder)
    df.to_pickle('./'+str(pD)+'/'+name+'.pkl')
    # Save yearly plots separately (years/pics-folder)
    try:
        plotYear(df,avl_skiCenters,par,name,years,pP)
    except Exception as e:
        print(e)
    # Delete dataframe to free space immediately
    del(df)

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

# Fill sites with yearly (winter) data
master = fillMaster(master,startWinter,pD)

# Do parameter specific tricks (if any)
master = parameterSpecific(master,par)

# Fill NaN values with linear interpolation
master = interpolateNaNs(master)

# Calculate statistics columns
master = calcRowStat(master)

# Plot site specific statistics
if rePlotSites:
    plotSite(master,par,startWinter,endWinter,siteToSki,siteToEst,pS)
