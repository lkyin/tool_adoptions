import json
import datetime
import os

############################################################################################################################################
prefix = '/data/GHArchive'

cnt = 0

author_knowledge_dict = {}

with open('/data/Adoption_data_new/commits/merged_dict.json', 'r') as jf:

    author_commit_histroy = json.load(jf)


with open('./data/tool_adoption_dict.json', 'r') as jf:

    adoptions = json.load(jf)

############################################################################################################################################


# old version based on data/commits/commits
def cal_exposure(author, project_name):

    if author not in author_knowledge_dict:

        author_knowledge_dict[author] = {}

    commits = author_commit_histroy[project_name][author]

    for commit_time in commits:

        for adoption in adoptions[project_name]:

            adopted_time = adoption[1]
            
            tool = adoption[2]

            if commit_time < adopted_time: 

                continue

            if tool not in author_knowledge_dict[author]:

                author_knowledge_dict[author][tool] = adopted_time

            else:

                author_knowledge_dict[author][tool] = min(author_knowledge_dict[author][tool], adopted_time)



for project_name in author_commit_histroy:

    cnt += 1

    #project_name = 'hybridgroup/cylon-neurosky'

    print('processing the {}th project'.format(cnt))

    for author in author_commit_histroy[project_name]:

        cal_exposure(author, project_name)


with open('/data/Adoption_data_new/authors/author_knowledge_dict.json', 'w') as jf:

    json.dump(author_knowledge_dict, jf, indent = 4)

print('all done!~~~')

















