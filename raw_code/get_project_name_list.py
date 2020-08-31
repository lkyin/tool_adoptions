import json
import datetime
from tqdm import tqdm
import concurrent.futures
from get_login import get_login
import requests
import random


def main(project_name):

    '''
    #input: developer_list, the repository name, the dictionary of member_experience
    #output: Issues and comments on the issue for this repo before tool adoption date.

    '''

    project_name = project_name.replace('\n', '')

    auth_set = get_login()

    headers = {'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

    # requests for comments on issues

    url = 'https://api.github.com/repos/{}/contributors'.format(project_name)

    #print(commits_url)

    r = requests.get(url, headers=headers, auth=random.choice(auth_set))

    if not r.ok:

        # print(r)

        # print(url)

        return []

    else:

        contributors = json.loads(r.text or r.content)

        if len(contributors) >= 10:

            print('get one!')

            return [project_name]

        else:

            return []

print ("Start loading...")

#Get the list of all projects names

print ('Loading the project_name_list...')

with open('data/contain_more_than_5_contributors.txt', 'r') as f:

    project_name_list = f.readlines()


#--------------------Start setting the parameters----------------------

current_number = 1

project_commits = {}

#--------------------End setting the parameters----------------------

print ('Processing the data...')

# project_name_list = project_name_list[:]

total_number = len(project_name_list)

rst_projects = []

with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:

    for project in executor.map(main, project_name_list):

        print('there are {} projects left'.format(total_number - current_number))
        
        current_number += 1

        rst_projects += project

with open('data/contain_more_than_10_contributors.txt', 'w') as f:

    for project in rst_projects:

        f.write(project)

        if project != rst_projects[-1]:

            f.write('\n')

        






