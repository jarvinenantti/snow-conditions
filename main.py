# coding=utf-8

'''
Fetch FMI open data using "fmiopendata"-library
https://github.com/pnuu/fmiopendata
pip install fmiopendata
numpy, requests, pandas, datetime, math, matplotlib, pathlib, os

Configured for 1.9. - 30.6. (~winter) !
'''

from createPaths import createPaths
from splitWinters import splitWinters
from checkAvailability import checkAvailability
from fetchFmiData import fetchFmiData
from toPandasDF import toPandasDF
from plotter import plotYear, plotSite, plotTimeseries
from fillMaster import fillMaster
from parameterSpecific import parameterSpecific
from interpolateNaNs import interpolateNaNs
from calcStat import calcRowStat, calcYearStat
from createTimeseries import createTimeseries

from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd


# Yearly inspection YES/NO
yearly = False

# Timeseries inspection YES/NO
timeseries = True

# Re-plot YES/NO
rePlotYears = False
rePlotSites = False
rePlotTS = True

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
paths = createPaths(years)
pD = paths[0]  # data
pP = paths[1]  # pics
pS = paths[2]  # sites

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


if yearly:
    # Fill sites with yearly (winter) data
    master = fillMaster(master,startWinter,pD)

    # Do parameter specific tricks (if any)
    master = parameterSpecific(master,par)

    # Fill NaNs using linear interpolation
    master = interpolateNaNs(master)

    # Calculate statistics columns
    master = calcRowStat(master)

    # Plot site specific statistics
    if rePlotSites:
        plotSite(master,par,startWinter,endWinter,siteToSki,siteToEst,pS)

    # Delete master file to free space
    del(master)


if timeseries:
    # Create timeseries-dataframes
    ts = createTimeseries(sites,pD)

    # Plot timeseries
    if rePlotTS:
        plotTimeseries(ts,par,startWinter,endWinter,siteToSki,siteToEst,pS,'unprocessed')

    # Delete timeseries to free space
    # del(ts)
