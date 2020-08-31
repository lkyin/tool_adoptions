import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################

time_leaving = 120

# least_commit_times = 2

young_threshold = 90

save_file_to = '/data/Adoption_data_new/result/num_tenure.json'

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

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


def is_young(project, author, time):

    author_commit_histroy[project][author].sort()

    first_commit_time = author_commit_histroy[project][author][0]

    # print(first_commit_time, time)

    gap = date_minus(first_commit_time, time)

    if gap < young_threshold:

        return True

    else:

        return False


exposure_dict = {}

for project in tqdm(project_list):

    exposure_dict[project] = {}

    for adoption in adoptions[project]:

        # print('-------------------------------')

        time = adoption[1]

        tool = adoption[2]

        exposure_dict[project][tool] = []

        interval = get_interval(time)

        for time_stamp in interval:

            active_members = get_active_developer(author_commit_histroy[project], project, time_stamp)

            if len(active_members) == 0:

                # print('[0, 0]')

                exposure_dict[project][tool].append(0)

                continue

            young_members = [is_young(project, member, time_stamp) for member in active_members]

            number_of_young_members = len([member for member in young_members if member])

            number_of_active_members = len(active_members)

            exposure_dict[project][tool].append(number_of_young_members)
            
            # exposure_dict[project][tool].append(float(number_of_active_members))

            # print([number_of_young_members, number_of_active_members])

            # print(number_of_active_members)

        # print('-------------------------------')

with open(save_file_to, 'w') as jf:

    json.dump(exposure_dict, jf, indent = 4)


print('all done!~~~')

















