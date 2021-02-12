import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import date as da


def plotYear(df,skiCenters,par,name):
    '''Plot yearly measurements'''

    plt.close("all")
    # Plot the entire dataframe
    df.plot()
    # Parameter as y-label
    plt.ylabel(par)
    # Set max y-limit for snow
    if par == 'snow_aws':
        plt.ylim(0,150) # 150 cm max for snow
    # Set ski centers as legend
    plt.legend(skiCenters)
    # Save figure
    plt.savefig('./pics/'+name+'.png')


def plotSite(data,par,startWinter,endWinter,siteToSki):
    '''Plot site statistics'''
    
    # Generate arbitrary year datetimes for better interpretability
    dates = mdates.drange(date(2049, 9, 1), date(2050, 7, 1), dt.timedelta(days=1))  

    plt.close("all")
    # Loop all sites
    for key in data.keys():
        # Select the site
        site = data[key]
        # Subplots required for filling areas
        fig, ax = plt.subplots()
        # Plot the mean
        ax.plot(dates, site['mean'], '-')
        # Plot the 50% quantile, alpha for transparency
        ax.fill_between(dates, site['q25'], site['q75'], color='C0', alpha=0.5)
        # Plot the 80% quantile
        ax.fill_between(dates, site['q10'], site['q25'], color='C1', alpha=0.2)
        ax.fill_between(dates, site['q75'], site['q90'], color='C1', alpha=0.2)
        # Set max y-limit for snow
        if par == 'snow_aws':
            ax.set_ylim(0,200) # 200 cm max for snow
        ax.set_ylabel(par)
        # Interpret the x-axis values as dates
        ax.xaxis_date()
        # Rotate x-axis ticks
        fig.autofmt_xdate()
        # Set title
        ax.set_title('mean, 50% quantile, and 80% quantile')
        # Save figure
        name = par+'_'+siteToSki[key]+'_'+str(startWinter)+'_'+str(endWinter)
        plt.savefig('./pics/'+name+'.png')
