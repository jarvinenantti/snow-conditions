import matplotlib.pyplot as plt

def plotter(df,sites):
    '''Plot measurements'''

    plt.close("all")
    # plt.figure()
    df.plot()
    plt.show()
