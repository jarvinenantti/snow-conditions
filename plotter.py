import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt


def plotYear(df,skiCenters,par,name,years,pP):
    '''Plot yearly measurements'''

    plt.close("all")
    # Plot the entire dataframe
    df.plot()
    # Parameter as y-label
    unit = df['unit'].iloc[0]
    plt.ylabel(par+' ('+unit+')')
    if par == 'snow_aws':
        # Set max y-limit 180 cm
        plt.ylim(0,180)
    # Set ski centers as legend
    plt.legend(skiCenters)
    # Save figure
    plt.savefig('./'+str(pP)+'/'+name+'.png')


def plotSite(data,par,startWinter,endWinter,siteToSki,siteToEst,pS):
    '''Plot site statistics'''
    
#     # Generate datetimes (arbitrary, no leap year) for better interpretability
#     dates = mdates.drange(dt.date(2049, 9, 1), dt.date(2050, 7, 1), dt.timedelta(days=1))  
    ticks = ['09-01','10-01','11-01','12-01','01-01','02-01','03-01','04-01','05-01','06-01']

    unit = ''
    begin = ''
    end = str(endWinter)

    plt.close("all")
    # Loop all sites
    for key in data.keys():
        # Select the site
        site = data[key]
        # Subplots required for filling areas
        fig, ax = plt.subplots()
#         # Plot the mean
#         ax.plot(dates, site['mean'], '-')
#         # Plot the 50% quantile, alpha for transparency
#         ax.fill_between(dates, site['q25'], site['q75'], color='C0', alpha=0.5)
#         # Plot the 80% quantile
#         ax.fill_between(dates, site['q10'], site['q25'], color='C1', alpha=0.2)
#         ax.fill_between(dates, site['q75'], site['q90'], color='C1', alpha=0.2)
        # Plot the mean
        ax.plot(site['date'], site['mean'], '-')
        # Plot the 50% quantile, alpha for transparency
        ax.fill_between(site['date'], site['q25'], site['q75'], color='C0', alpha=0.5)
        # Plot the 80% quantile
        ax.fill_between(site['date'], site['q10'], site['q25'], color='C1', alpha=0.2)
        ax.fill_between(site['date'], site['q75'], site['q90'], color='C1', alpha=0.2)
        # Set max y-limit for snow
        if par == 'snow_aws':
            ax.set_ylim(0,180) # 180 cm max for snow
            unit = '(cm)'
        ax.set_ylabel(par+' '+unit)
        #         # Interpret the x-axis values as dates
        #         ax.xaxis_date()
        #         ax.set_xticks(site['date'].values.tolist()[0::31])
        ax.set_xticks(ticks)
        # Rotate x-axis ticks
        fig.autofmt_xdate()
        # Site specific start year
        if siteToEst[key] > startWinter:
            begin = str(siteToEst[key])
        else:
            begin = str(startWinter)
        # Set title
        ax.set_title(siteToSki[key]+' '+begin+'-'+end+', mean, 50% quantile, and 80% quantile')
        # Save figure
        name = par+'_'+siteToSki[key]+'_'+begin+'_'+end
        plt.savefig('./'+str(pS)+'/'+name+'.png')


def plotDecomposition(data):
    ''' Plot components of timeseries'''

