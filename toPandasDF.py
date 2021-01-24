import pandas as pd

def toPandasDF(fmiData,sites):
    '''Create pandas df containing specific measurements'''
    
    df = pd.DataFrame() # all records
    for obs in fmiData:
        df2 = pd.DataFrame() # records from single period
        for site in sites:
            # Create a dataframe of single site
            d = obs.data[site]['snow_aws']
            dfS = pd.DataFrame(data = d) # single site, single period
            dfS = dfS.rename(columns={'values': site})
            dfS.drop(['unit'], axis=1)
            dfS.index = pd.to_datetime(obs.data[site]['times'])

            # Combine sites into single dataframe
            if df2.empty:
                df2 = pd.concat([df2,dfS])
            elif site not in df2:
                newPlace = dfS[site]
                df2 = df2.join(newPlace)
            else: # Site covers multiple places
                continue

        # Concatenate time periods
        df = pd.concat([df, df2])

    return(df)