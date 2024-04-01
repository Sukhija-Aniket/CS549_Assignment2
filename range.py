import pandas as pd
import os

data = []
def read_data(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:  # Skip the header line
        values = line.split()
        day_time = output_file.split('_')[1].split('.')[0]
        data.append([int(values[0]), int(values[1]), int(values[2]), day_time, float(values[3]), float(values[4])])

script_dir = os.path.dirname(__file__)
outputs_dir = os.path.join(script_dir, "outputs")
read_data(os.path.join(outputs_dir,'output_morning.txt'))
read_data(os.path.join(outputs_dir,'output_evening.txt'))
read_data(os.path.join(outputs_dir,'output_night.txt'))

columns = ['File_Size', 'Speed_Limit', 'Concurrent_Downloads', 'Time_of_Day', 'Total_Time', 'Throughput']

df = pd.DataFrame(data, columns=columns)

# file_size_filter = [1, 500000000]
file_size_filter = [10000000]
speed_limit_filter = [1000]
concurrent_downloads_filter = [1]
time_of_day_filter = ['night'] 

# File Size is the factor
file_df = df[
    (df['Speed_Limit'].isin(speed_limit_filter)) &
    (df['Concurrent_Downloads'].isin(concurrent_downloads_filter)) &
    (df['Time_of_Day'].isin(time_of_day_filter))].sort_values(by='File_Size')
file_df = file_df[['File_Size', 'Throughput']]
print(file_df.to_string(index=False))

# Speed Limit is the factor
speed_df = df[
    (df['File_Size'].isin(file_size_filter)) &
    # (df['Speed_Limit'].isin(speed_limit_filter)) &
    (df['Concurrent_Downloads'].isin(concurrent_downloads_filter)) &
    (df['Time_of_Day'].isin(time_of_day_filter))].sort_values(by='Speed_Limit')
speed_df = speed_df[['Speed_Limit', 'Throughput']]
print(speed_df.to_string(index=False))

# Concurrent Downloads is the factor
downloads_df = df[
    (df['File_Size'].isin(file_size_filter)) &
    (df['Speed_Limit'].isin(speed_limit_filter)) &
    # (df['Concurrent_Downloads'].isin(concurrent_downloads_filter)) &
    (df['Time_of_Day'].isin(time_of_day_filter))].sort_values(by='Concurrent_Downloads')
downloads_df = downloads_df[['Concurrent_Downloads', 'Throughput']]
print(downloads_df.to_string(index=False))

# Time of Day is the factor
time_df = df[
    (df['File_Size'].isin(file_size_filter)) &
    (df['Speed_Limit'].isin(speed_limit_filter)) &
    (df['Concurrent_Downloads'].isin(concurrent_downloads_filter))
    # (df['Time_of_Day'].isin(time_of_day_filter))
    ].sort_values(by='Time_of_Day')
time_df = time_df[['Time_of_Day', 'Throughput']]
print(time_df.to_string(index=False))



