# Fetch FMI open data using "fmiopendata"-library
# https://github.com/pnuu/fmiopendata
# pip install fmiopendata
# numpy, requests, pandas

from toPandasDF import toPandasDF
from fetchFmiData import fetchFmiData
from plotter import plotter

# Ski Centers: Saariselkä, Levi, Ylläs, Pallas (Ollos), Pyhä (Luosto), Ruka, Syöte, Vuokatti
skiCenters = ['Saariselkä','Levi','Ylläs','Pallas(Ollos)','Pyhä(Luosto)','Ruka','Syöte','Vuokatti']
# And closest FMI-sites with snow records
sites = ['Inari Saariselkä matkailukeskus','Kittilä kirkonkylä','Kittilä kirkonkylä','Kittilä Kenttärova','Kemijärvi lentokenttä','Kuusamo Kiutaköngäs','Taivalkoski kirkonkylä','Sotkamo Kuolaniemi']

# Define timeperiod
startTime = '2021-01-01T00:00:00'
endTime = '2021-01-03T00:00:00'

# Define parameter of interest
par = 'snow_aws' # snow cover

# Fetch data as a list of queries
fmiData = fetchFmiData(sites,startTime,endTime)
# print(type(fmiData))
# print(fmiData)
# print(fmiData[0].data[sites[0]]['snow_aws'])

# Cumulate all records of parameter intoto a single pandas dataframe
df = toPandasDF(fmiData,sites)
# print(df)
# cols = list(df.columns.values)
# print(cols)
# print(df.index)
# for ind in df.index:
#     print(ind)

# Plot measurements
# plotter(df,sites)

# name = par+startTime+endTime
df.to_pickle("./"+par+".pkl")
# unpickled_df = pd.read_pickle("./dummy.pkl")
