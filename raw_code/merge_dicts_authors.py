import os
import json


############################################################################################################################################
prefix = '/data/GHArchive'

year = ["2011", "2012", "2013", "2014", "2015","2016","2017","2018"]

month = ["01","02","03","04","05","06","07","08","09","10","11","12"]

day = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15", "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

hour = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14", "15","16","17","18","19","20","21","22","23"]

dict_by_projects = {}

dict_by_authors = {}

with open('data/final_project_list.txt', 'r') as f:

    project_list = f.readlines()

    project_list = set([project.replace('\n', '') for project in project_list])

############################################################################################################################################


for cur_year in year:

    for cur_month in month:

        for cur_day in day:

            print('{}-{}-{}'.format(cur_year, cur_month, cur_day))

            # project_dir = os.path.join(prefix, 'projects', cur_year, cur_month, (cur_day + '.json'))

            author_dir = os.path.join(prefix, 'authors', cur_year, cur_month, (cur_day + '.json'))

            try:

                '''

                with open(project_dir, 'r') as jf:

                    projects = json.load(jf)

                    dict_by_projects = {**dict_by_projects, **projects}

                '''
                with open(author_dir, 'r') as jf:

                    authors = json.load(jf)

                    for author in authors:

                        authors[author] = [event for event in authors[author] if (event[2] == 'PushEvent' or event[2] == 'CreateEvent' or event[2] == 'PullRequestEvent')]

                    dict_by_authors = {**dict_by_authors, **authors}
                

            except Exception as e:

                print(e)

                continue

'''
with open(os.path.join(prefix, 'projects', 'joint_projects.json'), 'w') as jf:

    json.dump(dict_by_projects, jf)
'''

with open('/data/Adoption_data/authors/authors.json', 'w') as jf:

    json.dump(dict_by_authors, jf)


print('all done!!!')











