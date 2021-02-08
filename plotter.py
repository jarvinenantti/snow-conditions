import matplotlib.pyplot as plt

def plotter(df,skiCenters,par,name):
    '''Plot measurements'''

    plt.close("all")
#     plt.figure()
    df.plot()
    plt.ylabel(par)
    if par == 'snow_aws':
        plt.ylim(0,150) # 150 cm max for snow
    plt.legend(skiCenters)
#     plt.show()
    
    # Save
    plt.savefig(name+'.png')
