'''
    filename: main.py
    main.py : main script
    author: Seoyeon Yang, Jeong Hyung Park, Su Jin Kang
    date  : 2018 July
    references:
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
import numpy as np
from preprocess.parsing import pars
import time
from datetime import datetime

'''
    filename: main.py
    main.py : main script
    author: Seoyeon Yang
    date  : 2019 August
    references: 
'''




def main():
    ## ---------------------------------------------------------------------------------------------------------------------
    ## data parser

    ## Save dir
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    nowdir = os.getcwd()
    board_logdir = "C:\\Users\\stella\\tensorboard\\"
    ckpt_logdir = "C:\\Users\\stella\\dev\\korean-audio-sentiment-analysis\\model\\check_point\\"

    if os.path.isfile("data_check.npy") == True:
        ans = np.load('data_check.npy')
        check = ans[0]
    else:
        data_check = np.array([0])
        check = 0
        np.save(nowdir, check)

    if check == 0:
        name = "\\data\\example_226.json"

        j_data = pars(os.path.join(nowdir, name))
        print(j_data)

if __name__ == "__main__":
     main()