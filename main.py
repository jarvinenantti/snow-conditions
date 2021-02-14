# coding=utf-8

'''
Fetch FMI open data using "fmiopendata"-library
https://github.com/pnuu/fmiopendata
pip install fmiopendata
numpy, requests, pandas, datetime, math, matplotlib, pathlib

Configured for 1.9. - 30.6. (~winter) !
'''


from splitWinters import splitWinters
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
    # If pickle-file exists, skip fetch and save, but recreate plots
    if Path('./data/'+name+'.pkl').is_file():
        print(name+' already exists, re-plot')
        if rePlot:
            df = pd.read_pickle(Path('./data/'+name+'.pkl'))
            plotYear(df,skiCenters,par,name)
        continue
    # Fetch data as a list of queries
    fmiData = fetchFmiData(sites,startTime,endTime)
    # Cumulate all records of parameter into a single pandas dataframe
    df = toPandasDF(fmiData,sites)
    # Save to pickle-files (data-folder)
    df.to_pickle("./data/"+name+".pkl")
    # Save yearly plots separately (pics-folder)
    plotYear(df,skiCenters,par,name)
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
master = fillMaster(master,startWinter)

# Do parameter specific tricks (if any)
master = parameterSpecific(master,par)

# Fill NaN values with linear interpolation
master = interpolateNaNs(master)

# Calculate statistics columns
master = calcStat(master)

# Plot site specific statistics
plotSite(master,par,startWinter,endWinter,siteToSki)
