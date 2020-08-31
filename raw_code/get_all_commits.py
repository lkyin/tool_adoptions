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

############################################################################################################################################
#--------------------Start setting the parameters----------------------
save_file_to = '/data/Adoption_data/commits/commits_CSCW.json'

headers = {'Accept':'application/vnd.github.squirrel-girl-preview+json'}

auth_set = get_login()

project_commits = {}

project_id = 1

with open('data/final_project_list.txt', 'r') as f:

    project_name_list = f.readlines()

    project_name_list = [project.replace('\n', '') for project in project_name_list]


#--------------------End setting the parameters----------------------
############################################################################################################################################


def process_text(commits):

    # process the commits on this page

    rst_commits = {}

    # process each commit
    for commit in commits:

        try:

            # get the author's login
            this_author = commit['author']['login']

            # get the commit date
            commit_date = commit['commit']['author']['date']

        except:

            # print(commit)

            continue

        # get the author's login of that commit
        # this_author = commit['commit']['author']['name']

        # get the commit url to futher retrieve the touched files
        # commit_url = commit['url']

        # files = []

        # r = requests.get(commit_url, headers=headers, auth=random.choice(auth_set))

        # if r.ok:

            # this_commit = json.loads(r.text or r.content)

            #files = [(file['filename'], file['additions'], file['deletions']) for file in this_commit['files']]

        # rst_commits.append([this_author, commit_date, files])

        if this_author not in rst_commits:

            rst_commits[this_author] = []

        rst_commits[this_author].append(commit_date)

    return rst_commits

def main(project_name):

    '''
    #input: developer_list, the repository name, the dictionary of member_experience
    #output: Issues and comments on the issue for this repo before tool adoption date.

    '''
    
    rst_commits = {}

    headers = {'Accept':'application/vnd.github.squirrel-girl-preview+json'}

    # requests for comments on issues

    commits_url = 'https://api.github.com/repos/{}/commits?per_page=100'.format(project_name)

    r = requests.get(commits_url, headers=headers, auth=random.choice(auth_set))

    if not r.ok:

        print(r)

        return [{}, None]

    else:

        pages_cnt = 1

        commits_of_this_page = json.loads(r.text or r.content)

        rst_commits = {**rst_commits, **process_text(commits_of_this_page)}

        while 'next' in r.links.keys():

            pages_cnt += 1

            r = requests.get(r.links['next']['url'], headers=headers, auth=random.choice(auth_set))

            if not r.ok:

                print(r)

                break

            else:

                commits_of_this_page = json.loads(r.text or r.content)

                rst_commits = {**rst_commits, **process_text(commits_of_this_page)}

    print('there are {} pages in commits'.format(pages_cnt))

    return [rst_commits, project_name]

print ("Start loading...")

# project_name_list = project_name_list[:]

total_number_of_projects = len(project_name_list)

with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:

#with concurrent.futures.ProcessPoolExecutor() as executor:

    for rst_commits, project_name in executor.map(main, project_name_list):

        if not project_name: continue # if this returns 403

        print('there are {} projects left'.format(total_number_of_projects - project_id))

        project_id += 1

        project_commits[project_name] = rst_commits

for project in project_commits:

    for author in project_commits[project]:

        project_commits[project][author].sort()

with open(save_file_to, 'w') as f:

    json.dump(project_commits, f, indent = 4)
