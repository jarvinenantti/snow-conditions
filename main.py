# coding=utf-8

'''
Fetch FMI open data using "fmiopendata"-library
https://github.com/pnuu/fmiopendata
pip install fmiopendata
numpy, requests, pandas, datetime, math, matplotlib, pathlib, os

Configured for 1.9. - 30.6. (~winter) !
'''

from splitWinters import splitWinters
from cutYears import cutYears
from fetchFmiData import fetchFmiData
from toPandasDF import toPandasDF
from plotter import plotYear, plotSite
from fillMaster import fillMaster
from parameterSpecific import parameterSpecific
from interpolateNaNs import interpolateNaNs
from calcStat import calcStat

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Re-plot ?
rePlot = False

# Ski Centers: Saariselkä, Levi, Ylläs/Pallas/Ollos, Pyhä/Luosto, Ruka, Syöte, Vuokatti, Kilpisjärvi
skiCenters = ['Saariselkä','Levi','Ylläs|Pallas|Ollos','Pyhä|Luosto','Ruka','Syöte','Vuokatti','Kilpisjärvi']

# And closest FMI-sites with snow records
sites = ['Inari Saariselkä matkailukeskus','Kittilä kirkonkylä','Kittilä Kenttärova','Kemijärvi lentokenttä','Kuusamo Kiutaköngäs','Taivalkoski kirkonkylä','Sotkamo Kuolaniemi','Enontekiö Kilpisjärvi kyläkeskus']

# Establishment year of the FMI site
# est = [1976, 2009, 2002, 2006, 1966, 2002, 1989, 1951] # 1989 wrong -> 2009 until further study
est = [1976, 2009, 2002, 2006, 1966, 2002, 2009, 1951]

# Define timeperiod in winters
startWinter = 1980
endWinter = 1990
assert endWinter > startWinter
years = str(startWinter)+'-'+str(endWinter)

# Generate data and path folders
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

# Generate timeperiods for winters
[startTimes,endTimes] = splitWinters(startWinter,endWinter)

# Example timeperiod (for past winters)
# startTime = '2020-09-01T00:00:00'
# endTime = '2021-06-30T00:00:00'
# Example timeperiod (for ongoing winter)
# startTime = '2020-09-01T00:00:00'
# endTime = '2021-02-20T00:00:00'

# Define parameter of interest
par = 'snow_aws' # snow cover

# Cut site and ski center lists according to data availability
[skiCenters,sites] = cutYears(skiCenters,sites,est,startWinter)

# Zip to dictionaries
siteToEst = dict(zip(sites, est))
siteToSki = dict(zip(sites, skiCenters))

# Fetch, transform and save year-by-year data and pics
for startTime,endTime in zip(startTimes,endTimes):
    
    # Create unique name for yearly parameter query
    name = par+'_'+startTime+'_'+endTime
    # If pickle-file exists, skip fetch and save, but recreate plots
    if Path('./'+years+'/data/'+name+'.pkl').is_file():
        print(name+' already exists, re-plot')
        if rePlot:
            df = pd.read_pickle(Path('./'+years+'/data/'+name+'.pkl'))
            plotYear(df,skiCenters,par,name)
        continue
    # Fetch data as a list of queries
    fmiData = fetchFmiData(sites,startTime,endTime)
    # Cumulate all records of parameter into a single pandas dataframe
    df = toPandasDF(fmiData,sites)
    # Save to pickle-files (years/data-folder)
    df.to_pickle('./'+years+'/data/'+name+'.pkl')
    # Save yearly plots separately (years/pics-folder)
    plotYear(df,skiCenters,par,name,years)
    # Delete dataframe
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
master = fillMaster(master,startWinter,years)

# Do parameter specific tricks (if any)
master = parameterSpecific(master,par)

# Fill NaN values with linear interpolation
master = interpolateNaNs(master)

# Calculate statistics columns
master = calcStat(master)

# Plot site specific statistics
plotSite(master,par,startWinter,endWinter,siteToSki)
