import json
import os
from tqdm import tqdm
import datetime
from scipy import stats
from collections import OrderedDict

###################################################################

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/comments1.1/sentiment_dict.json', 'r') as jf:

    sentiment_dict = json.load(jf)

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)


active_threshold = 90

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


def get_active_by_commit(project, time):

    active_devs_commit_set = set()

    for author in author_commit_histroy[project]:

        close_commit_time = None

        for commit_time in author_commit_histroy[project][author]:

            if commit_time < time: 

                close_commit_time = commit_time

            else: break

        if not close_commit_time: continue

        gap = date_minus(close_commit_time, time)

        if gap < active_threshold and gap > 0:

            active_devs_commit_set.add(author)

    return active_devs_commit_set

def get_active_by_comment(project, time):

    active_devs_comment_set = set()

    if project not in sentiment_dict:

        return active_devs_comment_set

    for author in sentiment_dict[project]:

        comment_history = sentiment_dict[project][author]

        close_comment_time = None

        for comment in comment_history:

            senti, comment_time, tool, is_adopted = comment

            if comment_time < time:

                close_comment_time = comment_time

            else: break

        if not close_comment_time: continue

        gap_days = date_minus(close_comment_time, time)

        if gap_days < active_threshold and gap_days > 0:

            active_devs_comment_set.add(author)

    return active_devs_comment_set


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

            if months <= -1 or months >= 1:

                continue

            rst_comments.append([author, senti, comment_time, tool])

    return rst_comments


active_devs_commit = OrderedDict()

active_devs_comment = OrderedDict()

active_devs_both = OrderedDict()


projects = list(sentiment_dict.keys())

for project in tqdm(projects):

    for tool in tool_adoption[project]:

        adoption_time =  tool_adoption[project][tool]

        time_interval = get_interval(adoption_time)

        for each_month in time_interval:

            index = time_interval.index(each_month)

            if index not in active_devs_commit: active_devs_commit[index] = []

            if index not in active_devs_comment: active_devs_comment[index] = []

            if index not in active_devs_both: active_devs_both[index] = []


            #------------------------------------#

            devs_comment = get_active_by_comment(project, each_month)

            devs_commit = get_active_by_commit(project, each_month)


            devs_both = devs_commit.union(devs_comment)

            #------------------------------------#

            active_devs_commit[index].append(len(devs_commit))

            active_devs_comment[index].append(len(devs_comment))

            active_devs_both[index].append(len(devs_both))

            #------------------------------------#


print([sum(active_devs_commit[each_month])/len(active_devs_commit[each_month]) 
      for each_month in active_devs_commit])

#-----------------------------------------------#

with open('./results/active_devs_commit.json', 'w') as jf:

    json.dump(active_devs_commit, jf)

with open('./results/active_devs_comment.json', 'w') as jf:

    json.dump(active_devs_comment, jf)

with open('./results/active_devs_both.json', 'w') as jf:

    json.dump(active_devs_both, jf)















