#coding: utf-8

"""
Created on Mon Mar 12 15:19:52 2019

@author: Likang Yin

"""

import requests
import datetime
import json
import pandas as pd
import numpy
import math
import copy
import random
import csv
import codecs
import re
import concurrent.futures
from get_login import get_login
from tqdm import tqdm


with open('results/comments/index.txt', 'r') as f:

    comments = eval(f.readlines()[0])

result_path = '/home/ylk1996/Code/Sentiment/Senti4SD/ClassificationTask/results.csv'

df = pd.read_csv(result_path, usecols = [])

sentiments = df.to_list()

final_dic = {}

for comment, sentiment in zip(comments, sentiments):

	project_name, this_tool, created_date, is_adopted = comment

	if project_name not in final_dic:

		final_dic[project_name] = {'adopted': [], 'non-adopted': []}


	if is_adopted:

		final_dic[project_name]['adopted'].append([created_date, sentiment])












