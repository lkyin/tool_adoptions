import json
import os
from tqdm import tqdm
import datetime

###################################################################

with open('data/final_project_list.txt', 'r') as f:

    projects = f.readlines()

    project_list = [project.replace('\n', '') for project in projects]

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/comments1.1/sentiment_dict.json', 'r') as jf:

    sentiment_dict = json.load(jf)

with open('/data/Adoption_data_new/commits/commits_CSCW.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

with open('/home/ylk1996/Research/CSCW1.1/data/adoptors.json', 'r') as jf:

    adoptors_dict = json.load(jf)

young_threshold = 90

##############################################################################


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


productivity_num = {'commits': {}, 'comments': {}}

productivity_frac = {'commits': {}, 'comments': {}}

for project in tqdm(project_list):

	adoptors = set()

	commits_by_young = 0

	commits_by_adoptor = 0

	comments_by_young = 0

	comments_by_adoptor = 0


	# get adoptors
	for tool in adoptors_dict[project]:

		for adoptor in adoptors_dict[project][tool]:

			adoptors.add(adoptor)

	# processing commits
	for author in author_commit_histroy[project]:

		first_commit_time = author_commit_histroy[project][author][0]

		for commit_time in author_commit_histroy[project][author]:

			if date_minus(first_commit_time, commit_time) < young_threshold:

				commits_by_young += 1

		if author in adoptors:

			commits_by_adoptor += len(author_commit_histroy[project][author])

	# add commits data to dict
	productivity_num['commits'][project] = [commits_by_young, commits_by_adoptor]
	productivity_frac['commits'][project] = commits_by_young/(commits_by_young+commits_by_adoptor)


	if project not in sentiment_dict:

		continue

	# processing commenting
	for author in sentiment_dict[project]:

		first_comment_time = sentiment_dict[project][author][0][1]

		for senti, comment_time, tool, is_adopted in sentiment_dict[project][author]:

			if author in adoptors:

				continue
			
			if date_minus(first_comment_time, comment_time) < young_threshold:

				comments_by_young += 1

		if author in adoptors:

			comments_by_adoptor += len(sentiment_dict[project][author])

	productivity_num['comments'][project] = [comments_by_young, comments_by_adoptor]

	if (comments_by_young+comments_by_adoptor) == 0:

		productivity_frac['comments'][project] = 0

	else:

		productivity_frac['comments'][project] = comments_by_young/(comments_by_young+comments_by_adoptor)


with open('./data/work_done_by_adoptors_num.json', 'w') as jf:

	json.dump(productivity_num, jf)


with open('./data/work_done_by_adoptors_frac.json', 'w') as jf:

	json.dump(productivity_frac, jf)

print(productivity_num['commits'])
























