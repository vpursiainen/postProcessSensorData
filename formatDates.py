import pandas as pd

def formatDatesAndTimes(data, occupancy):
    days = []
    times = []
    if occupancy == 0:
        row_name = 'collectedAt'
    else:
        row_name = 'createdAt'
    for index, row in data.iterrows():
        date = row[row_name]
        day = date[:10]
        time = date[11:19]
        days.append(day)
        times.append(time)
    data.insert(1,'Time', pd.Series(times))
    data.insert(1,'Day', pd.Series(days))
    del data[row_name]
    return data
