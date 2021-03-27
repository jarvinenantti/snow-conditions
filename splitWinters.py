import datetime as dt

def splitWinters(startWinter,endWinter,startDay,endDay):
    '''Split winters to separate timeperiods'''

    startTimes = []
    endTimes = []

    for i in range(startWinter,endWinter):
        s = str(i)
        e = str(i+1)
        startTimes.append(s+startDay)
        endTimes.append(e+endDay)

    return([startTimes,endTimes])
