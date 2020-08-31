import json
import os
from tqdm import tqdm
import datetime

###################################################################
path = '/data/Adoption_data_new/comments1.1/final_combinations/'

with open('./real_project_list.txt', 'r') as f:

    projects = f.readlines()

    project_list = [project.replace('\n', '') for project in projects]

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


young_devs = []

senior_devs = []


for project in tqdm(project_list[:]):

    if project not in sentiment_dict:

        # print('{} does not have comments'.format(project))

        continue

    for tool in tool_adoption[project]:

        adoption_time =  tool_adoption[project][tool]

        time_interval = get_interval(adoption_time)

        young_devs_l = []

        senior_devs_l = []

        for each_month in time_interval:

            young_devs_s = dict()

            senior_devs_s = dict()

            project_comments = sentiment_dict[project]

            comments_in = comments_in_period(each_month, project_comments)

            for comment in comments_in:

                author, senti, comment_time, tool = comment

                if senti != 'negative':

                    continue

                is_young_comment = is_young_by_comment(project, author, comment_time)

                is_young_commit = is_young_by_commit(project, author, comment_time)

                if (is_young_commit or is_young_comment):

                    if author not in young_devs_s:

                        young_devs_s[author] = 0

                    young_devs_s[author] += 1

                else:

                    if author not in senior_devs_s:

                        senior_devs_s[author] = 0

                    senior_devs_s[author] += 1
            

            if young_devs_s:

                young_devs_l.append(sum(young_devs_s.values())/len(young_devs_s.keys()))

            else:

                young_devs_l.append(0)


            if senior_devs_s:

                senior_devs_l.append(sum(senior_devs_s.values())/len(senior_devs_s.keys()))

            else:

                senior_devs_l.append(0)

        young_devs.append(young_devs_l)

        senior_devs.append(senior_devs_l)

# final_young = [sum(month)/len(month) for month in zip(*young_devs)]

# final_senior = [sum(month)/len(month) for month in zip(*senior_devs)]

#print(final_young)

#print(final_senior)

'''
with open('number_of_negative_comments_by_new.txt', 'w') as f:

    f.write(str(young_devs))

with open('number_of_negative_comments_by_senior.txt', 'w') as f:

    f.write(str(senior_devs))

'''
















