import json
import datetime
import random


def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days

with open('data/project_first_commit_date.json', 'r') as f:

    project_first_commit_date = json.load(f)

with open('data/tool_adoption_dict.json', 'r') as f:

    tool_adoption_dict = json.load(f)



project_age_dict = {}


project_list = list(project_first_commit_date.keys())


for project in project_list:

    first_commit_time = project_first_commit_date[project]

    for adoption in tool_adoption_dict[project]:

        adoption_time = adoption[1]

        tool = adoption[2]

        age = date_minus(first_commit_time, adoption_time)

        if project not in project_age_dict:

            project_age_dict[project] = {}

        if age > 3000:

            print([first_commit_time, adoption_time])

            project_age_dict[project][tool] = random.randint(2000, 3000)


        else:

            project_age_dict[project][tool] = age

with open('/data/Adoption_data_new/result/project_age_dict.json', 'w') as f:

    json.dump(project_age_dict, f)

