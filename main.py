# started 8:41 pm

import datetime

from typing import List
import math

REPORT_WIDTH = 120


class Entry:
    def __init__(self, date: str, state: str, cases: int):
        self.cases = cases
        self.state = state
        self.date: datetime.datetime = datetime.datetime.strptime(date, '%Y-%m-%d')

    def __repr__(self) -> str:
        return f"Cases: {self.cases} \nState: {self.state} \nDate: {self.date.strftime('%d-%m-%Y %H:%M')}\n"


def _format(text: str):
    numOfWhitespace = (REPORT_WIDTH - len(text)) // 2
    return ' ' * numOfWhitespace + text + ' ' * numOfWhitespace


def printReport(data: List[Entry], refDate: datetime.datetime, numOfStates: int):
    print(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}')
    print(_format('MALAYSIA COVID-19 NEW CASES ANALYSIS REPORT'))
    print(_format(f"Data Date : {max(map(lambda x: x.date, data)).strftime('%d-%m-%Y')}"))
    print(_format(f"Total New Cases : {sum(map(lambda x: x.cases, data)):,}"))
    print()
    print(_format(
        f"Reference Date {refDate.strftime('%d-%m-%Y')} (Total new cases : {sum(map(lambda x: x.cases, filter(lambda y: y.date >= refDate, data))):,})"))
    print()
    print()

    # header
    print(
        f"DAYS".ljust(10, ' ') +
        f"MALAYSIA".ljust(20, ' ') +
        f"HIGHEST 3 STATES".ljust(30, ' ').rjust(40, ' ') +
        f"LOWEST 3 STATES".ljust(30, ' ').rjust(40, ' ')
    )
    print(
        f" ".ljust(10, ' ') +
        f"DAILY AVERAGE".ljust(20, ' ') +
        f"NAME".ljust(20, ' ') +
        f"DAILY AVERAGE".ljust(20, ' ') +
        f"NAME".ljust(20, ' ') +
        f"DAILY AVERAGE".ljust(20, ' ')
    )
    print(
        '-' * REPORT_WIDTH
    )
    printLastNdays(7, refDate, allData)
    printLastNdays(30, refDate, allData)
    printLastNdays(90, refDate, allData)


def printLastNdays(n: int, refDate: datetime.datetime, data: List[Entry]):
    end = refDate - datetime.timedelta(days=n)

    dataFiltered = list(filter(lambda y: end < y.date <= refDate, data))

    dailyAverage = sum(map(lambda x: x.cases, dataFiltered)) / n

    collected = dict()

    for datum in dataFiltered:
        if datum.state not in collected.keys():
            collected[datum.state] = 0
        collected[datum.state] += datum.cases

    sortedCollected = sorted(collected.items(), key=lambda x: x[1], reverse=True)

    highest = sortedCollected[:3]
    lowest = sortedCollected[-3:][::-1]

    for i in range(len(highest)):
        tempDays = n
        tempDailyAvg = dailyAverage

        if i > 0:
            tempDays = None
            tempDailyAvg = None

        print(
            f"{tempDays if tempDays is not None else ''}".ljust(10, ' ') +
            f"{math.floor(tempDailyAvg) if tempDailyAvg is not None else ''}".ljust(20, ' ') +
            f"{highest[i][0]}".ljust(20, ' ') +
            f"{math.floor(highest[i][1] / n):,}".ljust(20, ' ') +
            f"{lowest[i][0]}".ljust(20, ' ') +
            f"{math.floor(lowest[i][1] / n):,}".ljust(20, ' ')
        )
    print()


def readCSV(csvFileLocation: str):
    masterList = []
    with open(csvFileLocation, 'r') as f:
        lines = f.readlines()[1:]
    for line in lines:
        data = line.split(',')
        masterList.append(
            Entry(data[0], data[1], int(data[2]))
        )
    return masterList


if __name__ == '__main__':
    refDate = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(
        days=10)  # yesterday
    numberOfStates = 3  # num of states
    allData = readCSV(r'./cases_state.csv')
    printReport(allData, refDate, numberOfStates)

# finished 10:38 pm
