import pandas as pd
import sys
from formatDates import formatDatesAndTimes

def processAndSave(sensor_file, occupancy_file):
    data = pd.read_csv(sensor_file)

    data = formatDatesAndTimes(data, 1)

    occupancy_data = pd.read_csv(occupancy_file)
    occupancy_data = occupancy_data.sort_values(by=['collectedAt'])
    occupancy_data = formatDatesAndTimes(occupancy_data, 0)

    days_grouped = data.groupby(['Day'])
    occupancy_day_grouped = occupancy_data.groupby(['Day'])

    ml_data = []
    ml_data.append('Time,Sound level (mV),Sound level (dB),Distance (cm),Light (full),Light (infrared),Light (visible),Temperature (C),Humidity (%),Occupancy\n')
    for day, day_group in days_grouped:
        grouped = day_group.groupby(['Time'])
        for time, date_group in grouped:
            date_data = [None] * 10
            date_data[0] = time
            date_data[9] = str(getOccupancy(occupancy_day_grouped.get_group(day), time))
            for row_ind, row in date_group.iterrows():
                if row['sensorName'] == 'Light':
                    date_data[4] = str(row['sensorValues.0.value'])
                    date_data[5] = str(row['sensorValues.1.value'])
                    date_data[6] = str(row['sensorValues.2.value'])
                elif row['sensorName'] == 'Distance sensor':
                    date_data[3] = str(row['sensorValues.0.value'])
                elif row['sensorName'] == 'Sound sensor':
                    date_data[1] = str(row['sensorValues.0.value'])
                    date_data[2] = str(row['sensorValues.1.value'])
                elif row['sensorName'] == 'TemperatureAndHumidity':
                    date_data[7] = str(row['sensorValues.0.value'])
                    date_data[8] = str(row['sensorValues.1.value'])
            ml_data.append(','.join(date_data) + '\n')

    out_file_name = 'PROCESSED_' + sensor_file
    with open(out_file_name, 'w+') as f_out:
        string_data = ''.join(str(line) for line in ml_data)
        f_out.write(string_data)

def getOccupancy(occupancy_data, date):
    n = 0
    for collection_date in occupancy_data['Time']:
        if n == 0:
            prev_date = collection_date
            if date < prev_date:
                row_index = occupancy_data.index[occupancy_data['Time']==prev_date].tolist()
                occupancy = occupancy_data.get_value(row_index[0], 'occupancy')
                return occupancy
            n = n + 1
        else:
            if (prev_date < date < collection_date):
                row_index = occupancy_data.index[occupancy_data['Time']==prev_date].tolist()
                occupancy = occupancy_data.get_value(row_index[0], 'occupancy')
                return occupancy
            prev_date = collection_date
    row_index = occupancy_data.index[occupancy_data['Time']==prev_date].tolist()
    occupancy = occupancy_data.get_value(row_index[0], 'occupancy')
    return occupancy

if __name__ == '__main__':
    processAndSave(*sys.argv[1:])
