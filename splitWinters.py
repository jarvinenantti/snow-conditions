import datetime as dt

def splitWinters(startWinter,endWinter):
    '''Split winters to separate timeperiods'''

    startTimes = []
    endTimes = []

    startS = '-09-01T00:00:00'
    endS = '-06-30T00:00:00'

    for i in range(startWinter,endWinter):
        s = str(i)
        e = str(i+1)
        startTimes.append(s+startS)
        endTimes.append(e+endS)

    return([startTimes,endTimes])
