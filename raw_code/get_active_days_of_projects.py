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

############################################################################################################################################
#--------------------Start setting the parameters----------------------

project_id = 1

with open("./data/project_first_commit_date.json", "r") as jf:

    first_commit_date = json.load(jf)

with open("./data/final_project_list.txt", "r") as f:

    project_name_list = f.readlines()

    project_name_list = [project.replace('\n', '') for project in project_name_list]

observation_end = '2018-03-01T15:37:50Z'

project_total_age = {}
#--------------------End setting the parameters----------------------
############################################################################################################################################


def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days
    


for project in project_name_list:

	fcd = first_commit_date[project]

	age = date_minus(fcd, observation_end)

	project_total_age[project] = age

with open('./data/project_total_age.json', 'w') as f:

    json.dump(project_total_age, f)


with open('/data/Adoption_data_new/model/final.csv', 'r') as f:

	final_lines = f.readlines()


avg_project = {}

first_line = final_lines[0]

features = first_line.split(',')

project, tool, project_age, time_to_adoption, ratio_young, num_young, ratio_exposure, num_exposure, ratio_active, num_active, ratio_negative, num_negative, ratio_involved, num_involved, num_commits, num_comments, num_positive_comments, num_negative_comments, status = features[1:20]


project_features = [project_age, time_to_adoption, ratio_young, num_young, ratio_exposure, num_exposure, ratio_active, num_active, ratio_negative, num_negative, ratio_involved, num_involved, num_commits, num_comments, num_positive_comments, num_negative_comments, status]
# print([project, tool, project_age, time_to_adoption, ratio_young, num_young, ratio_exposure, num_exposure, ratio_active, num_active, ratio_negative, num_negative, ratio_involved, num_involved, num_commits, num_comments, num_positive_comments, num_negative_comments, status])


for line in final_lines[1:]:

	line = line.replace('\n', '')

	features = line.split(',')

	project, tool, project_age, time_to_adoption, ratio_young, num_young, ratio_exposure, num_exposure, ratio_active, num_active, ratio_negative, num_negative, ratio_involved, num_involved, num_commits, num_comments, num_positive_comments, num_negative_comments, status = features[1:20]
	
	feature_values = [project_age, time_to_adoption, ratio_young, num_young, ratio_exposure, num_exposure, ratio_active, num_active, ratio_negative, num_negative, ratio_involved, num_involved, num_commits, num_comments, num_positive_comments, num_negative_comments, status]

	if project not in avg_project:

		avg_project[project] = {}

	if tool not in avg_project[project]:

		avg_project[project][tool] = {}

	for f, value in zip(project_features, feature_values):

		if f not in avg_project[project][tool]:

			avg_project[project][tool][f] = []

		avg_project[project][tool][f].append(float(value))

final_avg = {}

for project in avg_project:

	if project not in final_avg:

		final_avg[project] = {}

	for tool in avg_project[project]:

		if tool not in final_avg[project]:

			final_avg[project][tool] = {}

		for f in avg_project[project][tool]:

			# print(avg_project[project][tool][f])


			sum_ = sum(avg_project[project][tool][f])

			len_ = len(avg_project[project][tool][f])

			#print(avg_project[project][tool][f])

			final_avg[project][tool][f] = sum_ / len_


with open('./data/project_total_age.json', 'r') as f:

    project_total_age = json.load(f)

with open('./data/project_age_dict.json', 'r') as f:

	project_adoption_age = json.load(f)

with open('/data/Adoption_data_new/model/avg_record.csv', 'w') as csvf:

	csvf.write('project,tool,project_age,time_to_adoption,ratio_young,num_young,ratio_exposure,num_exposure,ratio_active,num_active,ratio_negative,num_negative,ratio_involved,num_involved,num_commits,num_comments,num_positive_comments,num_negative_comments,status\n')

	for project in final_avg:

		for tool in final_avg[project]:

			project_age = int(project_total_age[project]/2)

			time_to_adoption = int((project_age - project_adoption_age[project][tool])/30) 

			ratio_young = final_avg[project][tool]['ratio_young']

			num_young = int(final_avg[project][tool]['num_young'])

			ratio_exposure = final_avg[project][tool]['ratio_exposure']

			num_exposure = int(final_avg[project][tool]['num_exposure'])

			ratio_active = final_avg[project][tool]['ratio_active']

			ratio_negative = final_avg[project][tool]['ratio_negative']

			num_negative = int(final_avg[project][tool]['num_negative'])

			ratio_involved = final_avg[project][tool]['ratio_involved']

			num_involved = int(final_avg[project][tool]['num_involved'])

			num_active = int(final_avg[project][tool]['num_active'])

			num_commits = int(final_avg[project][tool]['num_commits'])

			num_comments = int(final_avg[project][tool]['num_comments'])

			num_positive_comments = int(final_avg[project][tool]['num_positive_comments'])

			num_negative_comments = int(final_avg[project][tool]['num_negative_comments'])

			status = 2

		csvf.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(

			project,tool,project_age,time_to_adoption,ratio_young,num_young,ratio_exposure,num_exposure,ratio_active,num_active,ratio_negative,num_negative,ratio_involved,num_involved,num_commits,num_comments,num_positive_comments,num_negative_comments,status)

		)
	

			

			

				










print('all done~')







