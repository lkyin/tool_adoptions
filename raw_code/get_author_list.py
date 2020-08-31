import json
import datetime
from tqdm import tqdm
import concurrent.futures
from get_login import get_login
import requests
import random



print ("Start loading...")

print ('Loading the project_name_list...')

with open('/data/Adoption_data_new/commits/commits_CSCW.json', 'r') as f:

    adoptions = json.load(f)


#--------------------Start setting the parameters----------------------

current_number = 1

authors_set = []

#--------------------End setting the parameters----------------------

print ('Processing the data...')

for project in adoptions:

	authors_of_this_project = list(adoptions[project].keys())

	authors_set += authors_of_this_project

# print(len(authors_set))

authors_set = set(authors_set)

print(len(authors_set))

num_of_authors = len(authors_set)

num = 0

with open('data/final_author_list.txt', 'w') as f:

    for author in authors_set:

        f.write(author)

        num += 1

        if num_of_authors != num:

            f.write('\n')

print('the number of total authors is {}'.format(num_of_authors))

        






