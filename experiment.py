import os
import time
import subprocess
import numpy as np
import sys
import random
from itertools import product


output_time = sys.argv[1]

# Directory to save downloaded files
script_dir = os.path.dirname(__file__)
download_dir = os.path.join(script_dir, "downloads")
outputs_dir = os.path.join(script_dir, "outputs")

# Create download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
else:
    for file in os.listdir(download_dir): 
        print("Removing file: ", os.path.join(download_dir, file))
        os.remove(os.path.join(download_dir, file)) # empty directory before starting the experiment

# Define file URLs
files = [
    'https://cloud.iitmandi.ac.in/f/104e18c7689843d38646/?dl=1', # a
    'https://cloud.iitmandi.ac.in/f/34f236050c354ac995dc/?dl=1', # b
    'https://cloud.iitmandi.ac.in/f/f2136456bcf6439eaf18/?dl=1', # c
    'https://cloud.iitmandi.ac.in/f/c3b76d27af45462db019/?dl=1', # d
    'https://cloud.iitmandi.ac.in/f/c3b76d27af45462db019/?dl=1', # e
    'https://cloud.iitmandi.ac.in/f/dcd4883d914a44fb9850/?dl=1', # f
    'https://cloud.iitmandi.ac.in/f/390c9e71032d4f30a6ca/?dl=1', # g
    'https://cloud.iitmandi.ac.in/f/4b2c32ec021e4de4a710/?dl=1', # h
    'https://cloud.iitmandi.ac.in/f/bf9f34fc8eec43ee991e/?dl=1', # i
]


# Define levels for factors
file_sizes = [1, 1000, 10000, 100000, 500000, 1000000, 10000000, 100000000, 500000000] # Bytes
file_sizes_idx = np.arange(0,9,1)
speed_limits = [1000, 2000, 4000, 8000]  # KB/s
concurrent_downloads = np.arange(1,9,2)

design_matrix = list(product(file_sizes_idx, speed_limits, concurrent_downloads))
k = 15
output_design = random.sample(design_matrix, k)

def download_files_second(file_idx, speed_limit, concur_downloads):
    processes = []
    url = files[file_idx]
    cmd = f"wget --limit-rate={speed_limit}k --directory-prefix={download_dir} {url} -q"
    start_time = time.time()
    for _ in range(concur_downloads):
        processes.append(subprocess.Popen(cmd, shell=True))
    for p in processes:
        p.wait()
    end_time = time.time()
    total_time = end_time - start_time
    file_size = file_sizes[file_idx]
    throughput = (concur_downloads * file_size)/ (total_time * 1e6) # Throughput in Mbps
    return total_time, throughput 

# Experiment
outputs = []
for sample in output_design:
    print(sample)
    idx = sample[0]
    speed = sample[1]
    concur_downloads = sample[2]
    day_time = output_time
    total_time, throughput = download_files_second(idx, speed, concur_downloads)
    print(total_time, throughput)
    output = f'{file_sizes[idx]} {speed} {concur_downloads} {day_time} {total_time} {throughput}'
    outputs.append(output)

output_file = f'results_{output_time}.txt'

with open(output_file, 'w') as file:
    file.write("File Size\tSpeed Limit (KB/s)\tConcurrent Downloads\tDownload Time (s)\tTotal Time\tThroughput (MB/s)\n")
    for output in outputs:
        file.write(output + '\n')


