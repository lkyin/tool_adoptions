import json
import os
from tqdm import tqdm
import datetime

###################################################################

with open('./project_list.txt', 'r') as f:
    projects = f.readlines()
    project_list = [eval(project).replace('\n', '') for project in projects]

with open('./tool_adoption.json', 'r') as f:
    tool_adoption = json.load(f)

with open('./sentiment_dict.json', 'r') as jf:
    sentiment_dict = json.load(jf)

with open('./merged_dict.json', 'r') as jf:
    author_commit_histroy = json.load(jf)

with open('./author_knowledge_dict.json', 'r') as jf:
    author_knowledge_dict = json.load(jf)


##############################################################################


def get_interval(comment_date):

    # two months(current month and one month before)

    date = datetime.datetime.strptime(comment_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-360, 360, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list


def is_exposed(author, time, tool, adoption_time):

    try:

        get_knowledge_date = author_knowledge_dict[author][tool]

    except:

        return False

    if get_knowledge_date == adoption_time:

        return False
    
    if get_knowledge_date < time:

        return True

    return False


def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


def comments_in_period(time, comments):

    rst_comments = []

    for author in project_comments:

        for comment in project_comments[author]:

            senti, comment_time, tool, is_adopted = comment

            days = date_minus(time, comment_time)

            months = days / 30

            if months < -1 or months > 1:

                continue

            rst_comments.append([author, senti, comment_time, tool])

    return rst_comments


exposed_devs = []

unexposed_devs = []


for project in tqdm(project_list):

    if project not in sentiment_dict:
        continue

    for tool in tool_adoption[project]:

        adoption_time =  tool_adoption[project][tool]

        time_interval = get_interval(adoption_time)

        exposed_devs_l = []

        unexposed_devs_l = []

        for each_month in time_interval:

            exposed_devs_s = dict()

            unexposed_devs_s = dict()

            project_comments = sentiment_dict[project]

            comments_in = comments_in_period(each_month, project_comments)

            for comment in comments_in:

                author, senti, comment_time, this_tool = comment

                if senti != 'negative': continue

                if_exposed = is_exposed(author, comment_time, tool, adoption_time)

                if if_exposed:

                    if author not in exposed_devs_s:

                        exposed_devs_s[author] = 0 

                    exposed_devs_s[author] += 1

                else:

                    if author not in unexposed_devs_s:

                        unexposed_devs_s[author] = 0 

                    unexposed_devs_s[author] += 1

            if exposed_devs_s:

                exposed_devs_l.append(sum(exposed_devs_s.values())/len(exposed_devs_s.keys()))

            else:

                exposed_devs_l.append(0)

            if unexposed_devs_s:
                
                unexposed_devs_l.append(sum(unexposed_devs_s.values())/len(unexposed_devs_s.keys()))

            else:

                unexposed_devs_l.append(0)
        exposed_devs.append(exposed_devs_l)
        unexposed_devs.append(unexposed_devs_l)

final_exposed = [sum(month)/len(month) for month in zip(*exposed_devs)]

final_unexposed = [sum(month)/len(month) for month in zip(*unexposed_devs)]

with open('negativity_exposure.csv', 'w') as f:
    f.write('group,month,num\n')

    for index, num in enumerate(final_exposed):
        month = index-11
        f.write('With Exposure,{},{}\n'.format(month, num))

    for index, num in enumerate(final_unexposed):
        month = index-11
        f.write('Without Exposure,{},{}\n'.format(month, num))


















