import os
import json

##################################### loading ##############################
with open('/data/Adoption_data_new/comments1.1/final_comm_comb_dict.json', 'r') as jsonf:

	comments = json.load(jsonf)

with open('/data/Adoption_data_new/commits/commits_CSCW.json', 'r') as jf:

	commits = json.load(jf)

##################################### End loading ##############################




young_by_comment = set()

young_by_commit = set()


def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days

def get_interval(adopted_date):

    date = datetime.datetime.strptime(adopted_date, '%Y-%m-%dT%H:%M:%SZ')

    time_list = []

    for i in range(-240, 120, 30):

        day = date + datetime.timedelta(days=i)

        day = str(day)

        day = day.replace(' ', 'T') + 'Z'

        time_list.append(day)

    return time_list
    
def get_begin_end_time(project, tool):

	pass

def get_young_by_commits(commits, begin_time, end_time):

	pass


def get_young_by_comments(comments, begin_time, end_time):

	pass


final_csv_path = '/data/Adoption_data_new/model/'

with open(final_csv_path + 'young_agg.csv', 'r') as f:

	csv_lines = f.readlines()


with open(final_csv_path + 'young_agg.csv', 'w') as f:

	f.write(csv_lines[0])

	for line in csv_lines[1:]:

		line = line.replace('\n', ',')

		features = line.split(',')

		project, tool = features[0], features[1]

		begin_time, end_time = get_begin_end_time(project, tool)

		young_by_comment = get_young_by_comments(comments, begin_time, end_time)

		young_by_commit = get_young_by_commits(commits, begin_time, end_time)



































