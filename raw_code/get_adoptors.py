import json
import datetime
from tqdm import tqdm


#--------------------Start setting the parameters----------------------

with open('data/final_project_list.txt', 'r') as f:

    project_name_list = f.readlines()

    project_name_list = [project_name.replace('\n', '') for project_name in project_name_list]

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/commits/commits_CSCW.json', 'r') as jf:

    author_commit_histroy = json.load(jf)

#--------------------End setting the parameters----------------------

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


def get_adoptors(project, ad_time):

	authors = author_commit_histroy[project]

	adoptors = set()

	for author in authors:

		for author_commit_time in authors[author]:

			if abs(date_minus(ad_time, author_commit_time)) <= 3:

				adoptors.add(author)

	return list(adoptors)


adoptors_dict = {}

for project in project_name_list:

	adoptors_dict[project] = {}

	for tool in tool_adoption[project]:

		ad_time = tool_adoption[project][tool]

		adoptors = get_adoptors(project, ad_time)

		adoptors = [adoptor for adoptor in adoptors if '[bot]' not in adoptor]

		if len(adoptors) == 0:

			adoptors = [project.split('/')[0]]

		adoptors_dict[project][tool] = adoptors

with open('data/adoptors.json', 'w') as jf:

    json.dump(adoptors_dict, jf, indent = 4)

print('all done~!!')

        






