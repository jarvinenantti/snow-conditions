import datetime as dt
from fmiopendata.wfs import download_stored_query
import math

def do7DaysQuery(sites,st,et):
      '''Query and return FMI-data (max 7 days)'''

      # Query type
      query = "fmi::observations::weather::multipointcoverage"

      # Define search space
      bbox = "bbox=20.5,64,30,70" # ~Lapland

      # Define the search time period (max 7 days for 1 query)
      start = "starttime="+st
      end = "endtime="+et
      timestep = "timestep=1440" # daily (1440 minutes)

      # Timeseries
      timeseries = "timeseries=True"

      # Execute query
      obs = download_stored_query(query,
                              args=[start,
                                    end,
                                    timestep,
                                    timeseries,
                                    bbox])

      # print(sorted(obs.data.keys()))
      # Pick sites of interest
      loc = []
      for place in sites:
            if len(obs.data[place]['times']) > 0:
                  loc.append(obs.data[place])
      # Check that data was successfully fetched
      assert len(loc) == len(sites)

      return(obs)


def fetchFmiData(sites,startTime,endTime):
      '''Execute the full data query and return all observations as a list'''
      obs = []

      # Check if requested period is more than 7 days
      start = dt.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
      end = dt.datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
      dif = end-start
      difH = dif.total_seconds()/3600

      if difH < 168: # 7 d = 168 h
            # Convert time to a proper format
            stq = start.isoformat(timespec="seconds") + "Z"
            etq = end.isoformat(timespec="seconds") + "Z"
            # One query is enough
            obs.append(do7DaysQuery(sites,stq,etq))

      else:
            # Split querys to 1 week periods
            startPoints = []
            endPoints = []
            n = math.ceil(difH/168)
            startPoints.append(start)
            i = 0
            while i < n-1:
                  endPoints.append(startPoints[i]+dt.timedelta(days=7))
                  startPoints.append(endPoints[i])
                  i += 1
            endPoints.append(end)

            # Execute queries one-by-one
            for i in range(len(startPoints)):
                  # Convert time to a proper format
                  stq = startPoints[i].isoformat(timespec="seconds") + "Z"
                  etq = endPoints[i].isoformat(timespec="seconds") + "Z"
                  obs.append(do7DaysQuery(sites,stq,etq))

      return(obs)