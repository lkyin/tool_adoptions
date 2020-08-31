import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################

time_leaving = 120

# least_commit_times = 2

save_file_to = '/data/Adoption_data_new/result/num_active.json'

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

def get_active_developer(all_commit_history, projects_name, time):

    #input: projects_url, time
    #output: the list of active developers

    '''
    commit_history[project][author]: [date1, date2, date3, ...]

    '''

    active_authors = set()

    for author in all_commit_history:

        commit_history = all_commit_history[author][:]

        #if len(commit_history) < least_commit_times:

        #    continue

        commit_history.append(time)

        commit_history.sort()

        # print(commit_history)

        time_index = commit_history.index(time)

        if time_index == 0: continue

        previous_commit_date = commit_history[time_index - 1]

        on_leave_time = date_minus(commit_history[time_index - 1], commit_history[time_index])

        # print(on_leave_time)
        if on_leave_time < time_leaving:

            active_authors.add(str(author))

    return active_authors


def get_interval(adopted_date):

    date = datetime.datetime.strptime(adopted_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-240, 120, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list


def get_knowledge_of_author(author, time, tool, author_knowledge_dict):

    try:

        get_knowledge_date = author_knowledge_dict[author][tool]

    except:

        # print('not this one')

        return False
    
    if get_knowledge_date < time:

        return True

    return False


exposure_dict = {}

for project in tqdm(project_list):

    # project = 'koajs/kick-off-koa'
    # project = 'hybridgroup/cylon-neurosky'

    exposure_dict[project] = {}

    for adoption in adoptions[project]:

        # print('------------------------------')

        time = adoption[1]

        # print('adoption time is {}'.format(time))

        tool = adoption[2]

        exposure_dict[project][tool] = []

        interval = get_interval(time)
        
        for time_stamp in interval:

            # print('this time is {}'.format(time_stamp))

            active_members = get_active_developer(author_commit_histroy[project], project, time_stamp)

            # print(active_members)

            if len(active_members) == 0:

                # print('[0, 0]')

                exposure_dict[project][tool].append(0)

                continue

            # knowledge_list = [get_knowledge_of_author(member, time_stamp, tool, author_knowledge_dict) for member in active_members]

            # number_of_exposed_members = len([member for member in knowledge_list if member])

            number_of_active_members = len(active_members)

            exposure_dict[project][tool].append(number_of_active_members)

            # print([number_of_exposed_members, number_of_active_members])

        # print('------------------------------')



with open(save_file_to, 'w') as jf:

    json.dump(exposure_dict, jf, indent = 4)


print('all done!~~~')










