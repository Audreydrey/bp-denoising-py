#!/usr/bin/env python3
import os
import subprocess
from os import listdir
from os.path import isfile, join
import csv
from decimal import Decimal
import numpy as np

# for all input images in input folder
#    run 10, 50, 100 iterations
#   write result to resultLog/

AVG = 1            #for any number of iterations, repeat 10 times (mean var std)
ITERS = [1]       # different number of iterations
INPUT_PATH= 'input/'
RENDER_OUTPUT = 'false' #don't render output image during evaluation

FIELD_NAME = ['image' , 'image_size', 'number_of_iter','duration_ms', 'render_output_image',
             'total_duration_ms','mean', 'var', 'std']
LOG_FILE = ['resultLog/resultLogAllDir.csv', 'resultLog/resultLog.csv']

# log mean var std for this img and number of iterations
def log_stat(logFile, img, it, all_durations):
    with open(logFile, mode='a') as csv_file: # 'a' = append
        writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAME)
        dur_mean = np.mean(all_durations)
        dur_sum = np.sum(all_durations)
        dur_var = np.var(all_durations)
        dur_std = np.std(all_durations)
        writer.writerow({'image': img, 'number_of_iter': it, 'total_duration_ms' : dur_sum,
                         'mean': dur_mean, 'var' : dur_var, 'std': dur_std})
  

# call denoise_all_dir
# log duration to csv for one call(in js)
# calculate total duration for 10 calls
def eval_py_all_dir(img, it, renderOutput):
    all_durations = []
    
    for i in range(AVG):
        value = subprocess.check_output(
            ['python3', 'denoise_alldirs.py', 
            img,            #image name
            str(it),        #number of iterations
            renderOutput,   #don't render output image
            'true'])        #eval mode
        # print("value from py all dir")
        # print(value)
        duration = Decimal(value.decode("utf-8"))
        all_durations.append(duration)
        print('running ' + img + ' in denoise_alldirs.py \n for ' + str(it) + ' iterations ' + str(i + 1) + " times")
        print('duration = ' + str(duration))
    
    log_stat('resultLog/resultLogAllDir.csv', img, it, all_durations)


def eval_py(img, it, renderOutput):
    all_durations = []
    
    for i in range(AVG):
        value = subprocess.check_output(
            ['python3', 'denoise.py', 
            img,            #image name
            str(it),        #number of iterations
            renderOutput,    #don't render output image
            'true'])        #eval mdoe
        # print("value from js all dir")
        duration = Decimal(value.decode("utf-8"))
        all_durations.append(duration)
        print('running ' + img + ' in denoise.py \n for ' + str(it) + ' iterations ' + str(i + 1) + " times")
        print('duration = ' + str(duration))
    
    log_stat('resultLog/resultLog.csv', img, it, all_durations)


if __name__=="__main__":

    #============ clear result log and write header ==================
    for csv_file in LOG_FILE :
        log = open(csv_file, 'r+')
        log.truncate(0) # need '0' when using r+
        log.close()

        # write log file header
        with open(csv_file, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAME)
            writer.writeheader()

#   ============= get input image set ================
    inputImgs = [f for f in listdir(INPUT_PATH) if f.endswith('png')]

    for img in inputImgs:
        for it in ITERS:
            eval_py_all_dir(img, it, RENDER_OUTPUT)
            eval_py(img, it, RENDER_OUTPUT)
            # read previous duration in previous 3 lines (number of iteration tested)
            #     calculate mean var std

    