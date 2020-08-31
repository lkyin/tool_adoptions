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

    contributors_set = set()

    

    auth_set = get_login()

    headers = {'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

    # requests for comments on issues

    url = 'https://api.github.com/repos/{}/contributors'.format(project_name)

    #print(commits_url)

    r = requests.get(url, headers=headers, auth=random.choice(auth_set))

    if not r.ok:

        print(r)

        return contributors_set

    else:

        contributors = json.loads(r.text or r.content)

        for contributor in contributors:

            contributors_set.add(contributor['login'])

        while 'next' in r.links.keys():

            url = r.links['next']['url']

            r = requests.get(url, headers=headers, auth=random.choice(auth_set))

            if not r.ok:

                print(r)

                return contributors_set

            contributors = json.loads(r.text or r.content)

            for contributor in contributors:

                contributors_set.add(contributor['login'])



        return contributors_set



print ("Start loading...")

print ('Loading the project_name_list...')

with open('data/final_project_list.txt', 'r') as f:

    project_name_list = f.readlines()

    project_name_list = [project_name.replace('\n', '') for project_name in project_name_list]


#--------------------Start setting the parameters----------------------

current_number = 1

authors_list = list()

#--------------------End setting the parameters----------------------

print ('Processing the data...')

total_number = len(project_name_list)

with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:

    for authors in executor.map(main, project_name_list):

        print('there are {} projects left'.format(total_number - current_number))
        
        current_number += 1

        authors_list += authors

authors_list = list(set(authors_list))

with open('data/contributors.txt', 'w') as f:

    for author in authors_list:

        f.write(author)

        if author != authors_list[-1]:

            f.write('\n')

print('the number of total authors is {}'.format(len(authors_list)))

        






