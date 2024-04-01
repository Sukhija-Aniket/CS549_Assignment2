from scipy.stats import f, f_oneway
import numpy as np
import pandas as pd

# Define the data (replace with your actual data)
data = []
file_data = [[] for _ in range(9)]
speed_data = [[] for _ in range(4)]
def read_data(output_file):
    with open(output_file, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:  # Skip the header line
        values = line.split()
        day_time = output_file.split('_')[1].split('.')[0]
        data.append([int(values[0]), int(values[1]), int(values[2]), day_time, float(values[3]), float(values[4])])


read_data('output_morning.txt')
read_data('output_evening.txt')
read_data('output_night.txt')

columns = ['File_Size', 'Speed_Limit', 'Concurrent_Downloads', 'Time_of_Day', 'Total_Time', 'Throughput']

df = pd.DataFrame(data, columns=columns)

# file_size_filter = [1, 500000000]
file_size_filter = [10000000]
speed_limit_filter = [1000]
concurrent_downloads_filter = [1]

# File Size is the factor
def gatherFileData(filter):
    file_df = df[
        (df['Speed_Limit'].isin(speed_limit_filter)) &
        (df['Concurrent_Downloads'].isin(concurrent_downloads_filter)) &
        (df['Time_of_Day'] == filter)].sort_values(by='File_Size')
    file_df = file_df[['Throughput']]
    for idx,value in enumerate(file_df.values):
        file_data[idx].append(value[0])

def gatherSpeedData(filter):
    speed_df = df[
        (df['File_Size'].isin(file_size_filter)) &
        (df['Concurrent_Downloads'].isin(concurrent_downloads_filter)) &
        (df['Time_of_Day'] == filter)].sort_values(by='Speed_Limit')
    speed_df = speed_df[['Throughput']]
    for idx,value in enumerate(speed_df.values):
        speed_data[idx].append(value[0])

gatherFileData('morning')
gatherFileData('evening')
gatherFileData('night')
gatherSpeedData('morning')
gatherSpeedData('evening')
gatherSpeedData('night')
# speed_data.pop()
print(speed_data)


def analyse(name, output_data):
    print(f"\n\n{name}:")

    # Calculate degrees of freedom
    df_between = len(output_data) - 1
    df_within = len(output_data[0]) * len(output_data) - len(output_data)

    # Calculate sum of squares
    grand_mean = np.mean(np.concatenate(output_data))
    ss_total = np.sum(np.fromiter(((x - grand_mean) ** 2 for arr in output_data for x in arr), dtype=np.ndarray))
    ss_between = np.sum(np.fromiter((len(group) * (np.mean(group) - grand_mean) ** 2 for group in output_data), dtype=np.ndarray))
    ss_within = (ss_total - ss_between)

    # Calculate mean squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # Calculate F-value
    f_value = ms_between / ms_within

    # Calculate F-critical value
    f_critical = f.ppf(0.95, df_between, df_within)

    # Display the results
    print("SSA (Between-Group Sum of Squares):", ss_between)
    print("SSE (Within-Group Sum of Squares):", ss_within)
    print("SST (Total Sum of Squares):", ss_total)
    print("MSA (Mean Square for Between-Group):", ms_between)
    print("MSE (Mean Square for Within-Group):", ms_within)
    print("F-value:", f_value)
    print("F-critical:", f_critical)

analyse("Analysis for File Size", file_data)
analyse("Analysis for Speed Limit", speed_data)