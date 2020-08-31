#coding: utf-8

"""
Created on Mon July 12 15:19:52 2019

@author: Likang Yin

"""

import datetime
import json
import pandas as pd
import math
import copy
import random
import csv
import codecs
import re
from get_login import get_login

def pay_tech_dept(project, tech_dept_files, starting_point, end_point):

    for author in project:

        time_list = [datetime.datetime.strptime(commit[0], '%Y-%m-%dT%H:%M:%SZ') for commit in project[author]]

        for t, commit_files in time_list:

            # during someone left
            if t > starting_point and t < end_point:

                # if there is no commit files...
                if len(commit_files) == 0:

                    continue

                for filename, additions, deletions in commit_files:

                    if file in tech_dept_files:

                        delay_days = (t - starting_point).days

                        print('{} commits to {} after {} days...'.format(author, file, delay_days))




def check_on_leave(project, project_name, threshold = 90):

    adoption_time = [datetime.datetime.strptime(adoption[1], '%Y/%m/%d %H:%M')  for adoption in tool_adoption_dict[project_name]]

    #print(adoption_time)

    for author in project:

        time_list = [datetime.datetime.strptime(commit[0], '%Y-%m-%dT%H:%M:%SZ') for commit in project[author]]

        for i in range(1, len(time_list)):

            gap = (time_list[i] - time_list[i-1]).days

            if gap > threshold:

                starting_point = time_list[i-1] # + datetime.timedelta(days=threshold)

                end_point = time_list[i]

                closing_days = float('inf')

                for time in adoption_time:

                    this_closing_days = abs((time - starting_point).days)

                    # if this tool adoption date is closer to the leaving time
                    if closing_days > this_closing_days:

                        closing_days = this_closing_days

                        if starting_point < time:

                            leave_type = 'BEFORE'

                        else:

                            leave_type = 'AFTER'

                if closing_days <= threshold:

                    print('{} left for {} days from {} to {}, {} days {} tool adoption'.format(
                    author, gap, starting_point, end_point, closing_days, leave_type))

#-----------------------------------------------------------------------

print ("Start loading...")

#Get the list of all projects names

print ('Loading tool adoption information...')

with open('data/commits.json', 'r') as f:

    commits = json.load(f)

for key in commits:

    print(commits[key])

    raise KeyError

with open('data/tool_adoption_dict.json', 'r') as f:

    tool_adoption_dict = json.load(f)


projects_commits = {}

for project in commits:

    projects_commits[project] = {}

    for commit in commits[project]:

        author, commit_time, files = commit

        if author not in projects_commits[project]:

            projects_commits[project][author] = []

        projects_commits[project][author].append([commit_time, files])


for project in projects_commits.keys():

    check_on_leave(projects_commits[project], project)




