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
import yaml
import concurrent.futures
from get_login import get_login

############################################################################################################################################
#--------------------Start setting the parameters----------------------
auth_set = get_login()

project_id = 1

headers = {'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

first_commit_date_dict = {}


with open("/data/Adoption_data_new/result/sentiment.json", "r") as f:

    project_name_list = json.load(f)

    project_name_list = list(project_name_list.keys())

with open("data/tool_adoption_dict.json", "r") as f:

    tool_adoption_dict = json.load(f)

#--------------------End setting the parameters----------------------
############################################################################################################################################


def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days
    

def get_first_commit_date(project_name):

    # get first commit date


    initial_commits_url = 'https://api.github.com/repos/{}/commits?per_page=100'.format(project_name)

    initial_r = requests.get(initial_commits_url, headers=headers, auth=random.choice(auth_set))

    if not initial_r.ok:

        # this project is not valid anymore
        print('project is not valid..')
        return [False, project_name]

    else:

        commits_of_this_page = json.loads(initial_r.text or initial_r.content)

        if 'last' in initial_r.links.keys():

            r = requests.get(initial_r.links['last']['url'], headers=headers, auth=random.choice(auth_set))

            # this project is not valid anymore
            if not r.ok: 

                print(r)

                # not a valid project
                return [False, project_name]

            else:

                commits_of_this_page = json.loads(r.text or r.content)

                while len(commits_of_this_page) != 0:

                    # Pop the very last commit
                    first_commit = commits_of_this_page.pop()

                    try:

                        # Find the date of the first commit
                        first_commit_date = first_commit['commit']['author']['date']

                        break

                    except TypeError as e:

                        print('The account of this author is deleted... Trying to find the next one')

                # Can not locate the date of first commit
                if not first_commit_date: return [False, project_name]
                
        else:

            while len(commits_of_this_page) != 0:

                # Pop the very last commit
                first_commit = commits_of_this_page.pop()

                try:

                    # Find the date of the first commit
                    first_commit_date = first_commit['commit']['author']['date']

                    break

                except TypeError as e:

                    print('The account of this author is deleted... Trying to find the next one')

            if not first_commit_date: return [False, project_name]

            
    return [first_commit_date, project_name]


project_name_list = project_name_list[:]

total_number_of_projects = len(project_name_list)

# remove some projects that do not saitisfy the conditions... 
with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:

    for first_commit_date, project_name in executor.map(get_first_commit_date, project_name_list):

        print ('{}'.format(total_number_of_projects-project_id))

        project_id += 1

        if first_commit_date:

            first_commit_date_dict[project_name] = first_commit_date


total_number_of_projects = len(first_commit_date_dict.keys())

print(len(project_name_list))
print('the size of the real project list is {}'.format(total_number_of_projects))

with open('data/project_first_commit_date.json', 'w') as f:

    json.dump(first_commit_date_dict, f)

