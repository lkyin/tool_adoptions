import json
import os
from tqdm import tqdm
import datetime

###################################################################

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/comments1.1/sentiment_dict.json', 'r') as jf:

    sentiment_dict = json.load(jf)

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

young_threshold = 90

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


def is_young_by_commit(project, author, time):

    if author not in author_commit_histroy[project]:

        return False

    first_commit_time = author_commit_histroy[project][author][0]

    gap = date_minus(first_commit_time, time)

    if gap < young_threshold and gap > 0:

        return True

    return False

def is_young_by_comment(project, author, time):

    if author not in sentiment_dict[project]:

        return False

    comment_history = sentiment_dict[project][author]

    first_comment_time = comment_history[0][1]

    gap = date_minus(first_comment_time, time)

    if gap < young_threshold and gap > 0:

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


num_negs_young_devs = 0

num_negs_senior_devs = 0


for project in tqdm(sentiment_dict.keys()):

    for tool in tool_adoption[project]:

        adoption_time =  tool_adoption[project][tool]

        time_interval = get_interval(adoption_time)

        for each_month in time_interval:

            project_comments = sentiment_dict[project]

            comments_in = comments_in_period(each_month, project_comments)

            for comment in comments_in:

                author, senti, comment_time, tool = comment

                if senti != 'neutral':

                    continue

                is_young_comment = is_young_by_comment(project, author, comment_time)

                is_young_commit = is_young_by_commit(project, author, comment_time)

                if (is_young_commit or is_young_comment):

                    # print(1)

                    num_negs_young_devs += 1

                else:

                    # print(2)

                    num_negs_senior_devs += 1



print(num_negs_young_devs)

print(num_negs_senior_devs)


















