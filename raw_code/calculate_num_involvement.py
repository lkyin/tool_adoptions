import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################
time_leaving = 120

sentiment_last = 90

# least_commit_times = 2

save_file_to = '/data/Adoption_data_new/result/num_involvement.json'

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

with open('./data/tool_adoption_dict.json', 'r') as jf:

    adoptions = json.load(jf)

with open('/data/Adoption_data_new/comments/sentiment_dict.json', 'r') as jf:

    sentiments = json.load(jf)

with open('./data/final_project_list.txt', 'r') as f:

    project_list = f.readlines()

    project_list = [project.replace('\n', '') for project in project_list]

project_list = list(sentiments.keys())

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


def involved_authors(project, tool, time):

    # author_sentiment_history = sentiments[project][author]

    author_set = set()

    for author in sentiments[project]:

        author_sentiment_history = sentiments[project][author]

        for sentiment in author_sentiment_history:

            senti, this_time, tool_name, is_this_tool = sentiment

            if tool_name == None:

                tool_name = tool

            # print(list(tool_name))

            if this_time < time and (tool_name == tool or tool_name == None): #and date_minus(this_time, time) < sentiment_last:

                author_set.add(author)

                break

    return list(author_set)

# [['MaxMEllon/comelon', 'eslint', '2016-03-12T09:02:13Z', False]

exposure_dict = {}


for project in tqdm(project_list):

    exposure_dict[project] = {}

    for adoption in adoptions[project]:

        time = adoption[1]

        tool = adoption[2]

        exposure_dict[project][tool] = []

        interval = get_interval(time)

        for time_stamp in interval:

            active_members = get_active_developer(author_commit_histroy[project], project, time_stamp)

            if len(active_members) == 0 or project not in sentiments:

                #print('[0, 0]')

                exposure_dict[project][tool].append(0)

                continue

            involved_members = involved_authors(project, tool, time_stamp)

            number_of_involved_members = len(involved_members)

            total_members = len([member for member in active_members if member not in involved_members]) + number_of_involved_members

            # exposure_dict[project][tool].append(number_of_involved_members/total_members)
            exposure_dict[project][tool].append(number_of_involved_members)

            # print(number_of_involved_members)


with open(save_file_to, 'w') as jf:

    json.dump(exposure_dict, jf, indent = 4)


print('all done!~~~')

















