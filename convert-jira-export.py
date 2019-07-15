#!/usr/bin/env python3

"""
 This script can be used to convert the cycletimes downloaded with https://github.com/DeloitteDigitalUK/jira-agile-metrics
"""

import csv
from datetime import date

def timeToState(dates):
    dateTimes = map(lambda t: date.fromisoformat(t) if t else None, dates)
    previousDate = next(dateTimes)
    previousIndex = 0
    result = []
    for (index, currentDate) in enumerate(dateTimes):
        correctedIndex = index + 1 # TODO replace next() call by a peek so that we don't have to do this
        if not currentDate:
            continue
        if currentDate > previousDate:
            result+=(currentDate-previousDate).days*[previousIndex]
        previousIndex=correctedIndex
        previousDate=currentDate
            
    result.append(len(dates)-1)
    return result


def run():
    with open('cycletime.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)
        stateColumnStart = header.index("Name")+1
        stateColumnEnd = header.index("Type") # index exclusive
        finalStatusColumn = header.index("Status")
        with open('cycletime-cleaned.csv', 'w') as cleanedFile:
            delimiter = ","
            for row in reader:
                # if not row[finalStatusColumn]=="Done":
                #     continue # Filters out tickets not in done, for example canceled tickets
                cleanedFile.write(delimiter.join(map(str, timeToState(row[stateColumnStart:stateColumnEnd])))+"\n")

def test():
    times=["2019-11-01", None, "2019-11-05", "2019-11-06"]
    result = timeToState(times)
    assert result==[0,0,0,0,2,3]

    times=["2019-11-01", "2019-11-01", "2019-11-01", "2019-11-06"]
    result = timeToState(times)
    assert result==[2,2,2,2,2,3]

test()

run()