import json
import datetime
import os
from tqdm import tqdm

############################################################################################################################################
time_leaving = 120

sentiment_last = 90

# least_commit_times = 2

save_file_to = '/data/Adoption_data_new/result/num_negative_comments.json'

#with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

#    author_commit_histroy = json.load(jf)

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

def get_num_comments(sentiments, projects_name, start_date, end_date):

    #input: projects_url, time
    #output: the list of active developers

    authors = sentiments[projects_name]

    num_comments = 0

    for author in authors:

        author_sentiment_history = authors[author]

        for sentiment in author_sentiment_history:

            senti, comment_date, tool_name, is_this_tool = sentiment

            if comment_date > start_date and comment_date < end_date and senti == 'negative':

                num_comments += 1

    return num_comments


def get_interval(adopted_date):

    date = datetime.datetime.strptime(adopted_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-240, 150, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list


# [['MaxMEllon/comelon', 'eslint', '2016-03-12T09:02:13Z', False]

exposure_dict = {}


for project in tqdm(project_list):

    exposure_dict[project] = {}

    for adoption in adoptions[project]:

        time = adoption[1]

        tool = adoption[2]

        exposure_dict[project][tool] = []

        interval = get_interval(time)

        for i in range(len(interval)-1):

            start_date = interval[i]

            end_date = interval[i+1]

            num_comments = get_num_comments(sentiments, project, start_date, end_date)
            
            exposure_dict[project][tool].append(num_comments)



with open(save_file_to, 'w') as jf:

    json.dump(exposure_dict, jf, indent = 4)


print('all done!~~~')

















