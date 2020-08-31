import json
import datetime

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

	commits = json.load(jf)


commits_distribution = {}

for project in commits:

	if project not in commits_distribution:

		commits_distribution[project] = {}

	for author in commits[project]:

		if author not in commits_distribution[project]:

			commits_distribution[project][author] = []

		author_commits = commits[project][author][:]

		first_commit_date = author_commits[0]

		for commit in author_commits:

			day = date_minus(first_commit_date, commit)

			commits_distribution[project][author].append(day)

with open('/data/Adoption_data_new/commits/commits_distribution_overtime.json', 'w') as jf:

	json.dump(commits_distribution, jf)

print('all done!~')


