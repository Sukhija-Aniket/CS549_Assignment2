import pandas as pd
import os

data = []
def read_data(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:  # Skip the header line
        values = line.split()
        data.append([int(values[0]), int(values[1]), int(values[2]), values[3], float(values[4]), float(values[5])])


script_dir = os.path.dirname(__file__)
outputs_dir = os.path.join(script_dir, "outputs")
read_data(os.path.join(outputs_dir,'results_simple_morning.txt'))
read_data(os.path.join(outputs_dir,'results_simple_night.txt'))

columns = ['File_Size', 'Speed_Limit', 'Concurrent_Downloads', 'Time_of_Day', 'Total_Time', 'Throughput']

df = pd.DataFrame(data, columns=columns)

file_size_filter = [1, 500000000]
speed_limit_filter = [1000, 4000]
concurrent_downloads_filter = [1, 5]
# time_of_day_filter = ['morning', 'night'] # Not needed using morning, night values only

filtered_df = df[
    (df['File_Size'].isin(file_size_filter)) &
    (df['Speed_Limit'].isin(speed_limit_filter)) &
    (df['Concurrent_Downloads'].isin(concurrent_downloads_filter))]

sorted_df = filtered_df.sort_values(by='Throughput')

print(sorted_df)




