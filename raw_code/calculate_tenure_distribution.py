import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################

time_leaving = 120

# least_commit_times = 2

young_threshold = 180

save_file_to = '/data/Adoption_data_new/result/tenure_distribution.txt'

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

with open('./data/tool_adoption_dict.json', 'r') as jf:

    adoptions = json.load(jf)

with open('./data/final_project_list.txt', 'r') as f:

    project_list = f.readlines()

    project_list = [project.replace('\n', '') for project in project_list]

############################################################################################################################################

def get_interval(adopted_date):

    date = datetime.datetime.strptime(adopted_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-240, 120, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


lasting_time_list = []

for project in tqdm(project_list):

    for adoption in adoptions[project]:

        time = adoption[1]

        tool = adoption[2]

        interval = get_interval(time)

        starting_date = interval[0]

        ending_date = interval[-1]

        authors = list(author_commit_histroy[project].keys())

        for author in authors:

            commits_list = []

            for commit in author_commit_histroy[project][author]:

                if commit > starting_date and commit < ending_date:

                    commits_list.append(commit)

            if len(commits_list) < 2:

                continue

            else:

                first_commit_date = commits_list[0]

                last_commit_date = commits_list[-1]

                lasting_time = date_minus(first_commit_date, last_commit_date)

                if lasting_time == 0:

                    continue

                lasting_time_list.append(lasting_time)

print(sum(lasting_time_list)/len(lasting_time_list))

print(len(lasting_time_list))





with open(save_file_to, 'w') as f:

    f.writelines(str(lasting_time_list))


print('all done!~~~')

















