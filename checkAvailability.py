
def checkAvailability(skiCenters,sites,startTime,endTime,est,excl):
    '''Choose sites and ski centers according to the
    FMI site establishment year, and excluded years'''
    
    # Parse years
    startYear = int(startTime[0:4])
    endYear = int(endTime[0:4])
    
    # Create copies of lists
    avl_skiCenters = skiCenters.copy()
    avl_sites = sites.copy()

    # Iterate lists in reverse
    for i in range(len(sites)-1,-1,-1):
        # First check whether site was established
        if est[i] > startYear:
            avl_skiCenters.pop(i)
            avl_sites.pop(i)
            continue
        # Secondly check whether year is excluded
        for e in excl[i]:
            if e == startYear:
                avl_skiCenters.pop(i)
                avl_sites.pop(i)
                continue
    
    return(avl_skiCenters,avl_sites)