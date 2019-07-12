# postProcessSensorData

# Usage
python postprocessData.py sensor_data_csv_file occupancy_data_csv_file

e.g. python postprocessData.py 2019_07_12_test_sensor_data.csv 2019_07_12_test_occupancy_data.csv

# Input
Input sensor data file should have following columns: [_id	createdAt, macAddress, sensorName, sensorType, sensorValues.0.key, sensorValues.0.value, sensorValues.1.key, sensorValues.1.value, sensorValues.2.key, sensorValues.2.value]

Input occupancy file should have following columns: [_id, collectedAt, occupancy]

# Output

Outputs a processed CSV file with name POSTPROCESSED_ + original file name

Output CSV file has following columns: [Time, Sound level (mV), Sound level (dB), Distance (cm), Light (full), Light (infrared), Light (visible), Temperature (C), Humidity (%), Occupancy]

