# coding=utf-8

# Fetch FMI open data using "fmiopendata"-library
# https://github.com/pnuu/fmiopendata
# pip install fmiopendata
# numpy, requests, pandas, datetime, math, matplotlib

from toPandasDF import toPandasDF
from fetchFmiData import fetchFmiData
from plotter import plotter
from splitWinters import splitWinters
from pathlib import Path

# Ski Centers: Saariselkä, Levi, Ylläs, Pallas (Ollos), Pyhä (Luosto), Ruka, Syöte, Vuokatti, Kilpisjärvi
skiCenters = ['Saariselkä','Levi','Ylläs/Pallas/Ollos','Pyhä/Luosto','Ruka','Syöte','Vuokatti','Kilpisjärvi']
# And closest FMI-sites with snow records
sites = ['Inari Saariselkä matkailukeskus','Kittilä kirkonkylä','Kittilä kirkonkylä','Kittilä Kenttärova','Kemijärvi lentokenttä','Kuusamo Kiutaköngäs','Taivalkoski kirkonkylä','Sotkamo Kuolaniemi','Enontekiö Kilpisjärvi kyläkeskus']

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

# Fetch, transform and save year-by-year
for startTime,endTime in zip(startTimes,endTimes):
    
    # Create unique name for yearly parameter query
    name = par+'_'+startTime+'_'+endTime
    # If pickle-file exists, skip
    if Path(name+'.pkl').is_file():
        continue
    # Fetch data as a list of queries
    fmiData = fetchFmiData(sites,startTime,endTime)
    # Cumulate all records of parameter into a single pandas dataframe
    df = toPandasDF(fmiData,sites)
    # Save to pickle-files
    df.to_pickle("./"+name+".pkl")
    # Plot measurements
    plotter(df,skiCenters,par,name)

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
