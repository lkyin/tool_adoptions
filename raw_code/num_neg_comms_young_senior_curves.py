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

            if months <= -1 or months >= 1:

                continue

            rst_comments.append([author, senti, comment_time, tool])

    return rst_comments


young_devs = OrderedDict()

senior_devs = OrderedDict()

projects = list(sentiment_dict.keys())

for project in tqdm(projects):

    for tool in tool_adoption[project]:

        adoption_time =  tool_adoption[project][tool]

        time_interval = get_interval(adoption_time)

        cnt = 0

        for each_month in time_interval:

            index = time_interval.index(each_month)

            if index not in young_devs:

                young_devs[index] = {}

            if index not in senior_devs:

                senior_devs[index] = {}

            project_comments = sentiment_dict[project]

            comments_in = comments_in_period(each_month, project_comments)

            # print(len(comments_in))

            for comment in comments_in:

                author, senti, comment_time, tool = comment

                if senti != 'negative':

                    continue

                # print(1)

                is_young_comment = is_young_by_comment(project, author, comment_time)

                is_young_commit = is_young_by_commit(project, author, comment_time)


                if (is_young_commit or is_young_comment):

                    if author not in young_devs[index]:

                        young_devs[index][author] = 0

                    young_devs[index][author] += 1

                    

                else:

                    if author not in senior_devs[index]:

                        senior_devs[index][author] = 0

                    senior_devs[index][author] += 1


total_negativity_young = []

total_negativity_senior = []


for each_month in young_devs:

    #print(each_month)

    cnt = []

    for young_dev in young_devs[each_month]:

        #cnt += young_devs[each_month][young_dev]

        cnt.append(young_devs[each_month][young_dev])

    total_negativity_young.append(cnt)

        

for each_month in senior_devs:

    #print(each_month)

    cnt = []

    for senior_dev in senior_devs[each_month]:

        # cnt += senior_devs[each_month][senior_dev]

        cnt.append(senior_devs[each_month][senior_dev])
    
    total_negativity_senior.append(cnt)

# print(total_negativity_young)

# print(total_negativity_senior)

young_dev_dict = {}

for each_month in young_devs:

    for dev in young_devs[each_month]:

        if dev not in young_dev_dict:

            young_dev_dict[dev] = []


senior_dev_dict = {}

for each_month in senior_devs:

    for dev in senior_devs[each_month]:

        if dev not in senior_dev_dict:

            senior_dev_dict[dev] = []

# calculate the negativity by young devs
for each_month in young_devs:

    for dev in young_dev_dict:

        if dev in young_devs[each_month]:

            young_dev_dict[dev].append(young_devs[each_month][dev])

        else:

            young_dev_dict[dev].append(0)


# calculate the negativity by young devs
for each_month in senior_devs:

    for dev in senior_dev_dict:

        if dev in senior_devs[each_month]:

            senior_dev_dict[dev].append(senior_devs[each_month][dev])

        else:

            senior_dev_dict[dev].append(0)


#print(young_dev_dict)

#print(senior_dev_dict)


relative_negativity_young = []

relative_negativity_senior = []


for dev in senior_dev_dict:

    #avg = sum(senior_dev_dict[dev])/len(senior_dev_dict[dev])

    #relative_negativity_senior.append([neg/avg for neg in senior_dev_dict[dev]])

    negativity = senior_dev_dict[dev]

    relative_negativity_senior.append(stats.zscore(negativity).tolist())

for dev in young_dev_dict:

    # avg = (sum(young_dev_dict[dev])/len(young_dev_dict[dev]))

    # relative_negativity_young.append([neg/avg for neg in young_dev_dict[dev]])

    negativity = young_dev_dict[dev]

    relative_negativity_young.append(stats.zscore(negativity).tolist())


#relative_negativity_young = [sum(slot)/len(slot) for slot in zip(*relative_negativity_young)]

#relative_negativity_senior = [sum(slot)/len(slot) for slot in zip(*relative_negativity_senior)]


#-----------------------------------------------#

with open('./results/total_negativity_young.txt', 'w') as f:

    f.write(str(total_negativity_young))

with open('./results/total_negativity_senior.txt', 'w') as f:

    f.write(str(total_negativity_senior))

#-----------------------------------------------#

with open('./results/relative_negativity_young.txt', 'w') as f:
    
    f.write(str(relative_negativity_young))
    

with open('./results/relative_negativity_senior.txt', 'w') as f:

    f.write(str(relative_negativity_senior))

















