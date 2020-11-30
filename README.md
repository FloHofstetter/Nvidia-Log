# Nvidia-Log
Python Project to log and plot NVIDIA-SMI data.

# Getting started:
## 1. Install required packages
They only required packages are matplotlib and nvsmi  
`pip install requirements.txt`

## 2. Logg your GPUs
Files are named `GPU-<gpu-id>_<date>_<time>.csv`  
`python3 log.py`

## 3. Plot your GPU logs
Files are named with respect to the last comand line argument.  
`python3 plot.py <logfile_0.csv> <logfile_1.csv> <logfile_n.csv>`
