import json
import datetime
import copy

with open('commits_by_project.json', 'r') as f:

    projects = json.load(f)

new_project = {}

final_author_commit_history = {}

cnt = 0

team_size = 5

for projectname in projects.keys():

    new_project[projectname] = {}

    final_author_commit_history[projectname] = {}

    for author, commit_date in projects[projectname]:

        if author not in new_project.keys():

            new_project[projectname][author] = []

        new_project[projectname][author].append(commit_date)

    if len(new_project[projectname].keys()) >= team_size:

        final_author_commit_history[projectname] = new_project[projectname]


with open('author_commits_date.json', 'w') as f:

    json.dump(final_author_commit_history, f)







    
