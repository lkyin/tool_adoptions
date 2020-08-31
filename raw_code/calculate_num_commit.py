import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################

time_leaving = 120

# least_commit_times = 2

save_file_to = '/data/Adoption_data_new/result/num_commits.json'

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

with open('/data/Adoption_data_new/authors/author_knowledge_dict.json', 'r') as jf:

    author_knowledge_dict = json.load(jf)

with open('./data/tool_adoption_dict.json', 'r') as jf:

    adoptions = json.load(jf)

with open('./data/final_project_list.txt', 'r') as f:

    project_list = f.readlines()

    project_list = [project.replace('\n', '') for project in project_list]

############################################################################################################################################

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days

def get_num_commits(all_commit_history, projects_name, start_time, end_time):

    #input: projects_url, time
    #output: the list of active developers

    num_of_commits = 0

    authors = all_commit_history[projects_name]

    for author in authors:

        commit_history = authors[author][:]

        commit_history = commit_history[:].sort()

        for commit_date in commit_history:

            if commit_date > start_time and commit_date < end_time:

                print(start_time, end_time, commit_date)

                num_of_commits += 1

    return num_of_commits



def get_interval(adopted_date):

    date = datetime.datetime.strptime(adopted_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-240, 150, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list




exposure_dict = {}

for project in tqdm(project_list):

    # project = 'koajs/kick-off-koa'
    # project = 'hybridgroup/cylon-neurosky'

    exposure_dict[project] = {}

    for adoption in adoptions[project]:

        time = adoption[1]

        tool = adoption[2]

        exposure_dict[project][tool] = []

        interval = get_interval(time)
        
        for i in range(len(interval)-1):

            start_time = interval[i]

            end_time = interval[i+1]
            
            number_of_commits = get_num_commits(author_commit_histroy, project, start_time, end_time)

            exposure_dict[project][tool].append(number_of_commits)



with open(save_file_to, 'w') as jf:

    json.dump(exposure_dict, jf, indent = 4)


print('all done!~~~')










