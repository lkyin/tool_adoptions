import json
import datetime
import os
import gzip
import shutil
import codecs
import concurrent.futures
import re



############################################################################################################################################
prefix = '/data/GHArchive'

year = ["2011","2012","2013","2014", "2015","2016","2017","2018"]

month = ["01","02","03","04","05","06","07","08","09","10","11","12"]

day = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15", "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

hour = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14", "15","16","17","18","19","20","21","22","23"]

############################################################################################################################################


with open('./data/tool_adoption_dict.json', 'r') as f:

    adoptions = json.load(f)


with open('./data/final_project_list.txt', 'r') as f:

    projects = f.readlines()

    projects = set([project.replace('\n', '') for project in projects])

with open('./data/final_author_list.txt', 'r') as f:

    authors = f.readlines()

    authors = set([author.replace('\n', '') for author in authors])

############################################################################################################################################


def process_file(event, dict_by_projects_temp, dict_by_authors_temp):

    try:

        event_type = event['type']

        repo = event['repo']['name']

        author = event['actor']['login']

        time = event['created_at']

    except:

        return [dict_by_projects_temp, dict_by_authors_temp]

    # ------------------process dict_by_projects-----------------------------------
    '''
    if event_type == 'PushEvent' and repo in projects:

        if repo not in dict_by_projects_temp:

            dict_by_projects_temp[repo] = {}

        if author not in dict_by_projects_temp[repo]:

            dict_by_projects_temp[repo][author] = []

        dict_by_projects_temp[repo][author] += [commit['url'] for commit in event['payload']['commits']]

    '''

    # ------------------process dict_by_authors----------------------------------

    if event_type != 'PushEvent': return [dict_by_projects_temp, dict_by_authors_temp]

    if author in authors and repo in projects:

        if author not in dict_by_authors_temp:

            dict_by_authors_temp[author] = []

        dict_by_authors_temp[author].append([time, repo, event_type])

    return [dict_by_projects_temp, dict_by_authors_temp]


def main(time):

    global cnt

    dict_by_projects_temp = {}

    dict_by_authors_temp = {}

    cur_year, cur_month, cur_day, cur_hour, dict_by_projects, dict_by_authors = time

    timename = cur_year + '-' + cur_month +'-' + cur_day + '-' + cur_hour 

    print('processing {}...'.format(timename))

    filename =  os.path.join(prefix, 'raw_data', cur_year, cur_month, cur_day, "{}.json.gz".format(timename))

    jsonname =  os.path.join(prefix, 'raw_data', cur_year, cur_month, cur_day, "{}.json".format(timename))

    try:

        with gzip.open(filename, 'rb') as s_file, open(jsonname, 'wb') as d_file:

            shutil.copyfileobj(s_file, d_file)

    except:

        print('something wrong...{} does not exist...'.format(filename))

        return [dict_by_projects_temp, dict_by_authors_temp]

    with open(jsonname, 'r') as f:

        for line in f:
  
            try:

                dic = json.loads(line)

            except Exception as e:

                cnt += 1

                continue  


            rst_dict_by_projects, rst_dict_by_authors = process_file(dic, dict_by_projects_temp, dict_by_authors_temp)

            # dict_by_projects_temp = dict(dict_by_projects_temp, **rst_dict_by_projects)

            dict_by_authors_temp = dict(dict_by_authors_temp, **rst_dict_by_authors)

    os.remove(jsonname)

    return [dict_by_projects_temp, dict_by_authors_temp]

last_save_point = '2015-08-06'

for cur_year in year:

    for cur_month in month:

        for cur_day in day:

            timename = cur_year + '-' + cur_month +'-' + cur_day

            print(timename)

            if timename < last_save_point:

                continue

            cnt = 0

            dict_by_projects = {}

            dict_by_authors = {}

            dirname = os.path.join(prefix, cur_year, cur_month, cur_day)

            times = [[cur_year, cur_month, cur_day, cur_hour, dict_by_projects, dict_by_authors] for cur_hour in hour]

            #-----------------------------------------------------
            
            with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:

                # for dict_by_projects_temp, dict_by_authors_temp in executor.map(main, times):

                for dict_by_projects_temp, dict_by_authors_temp in executor.map(main, times):

                    # dict_by_projects = dict(dict_by_projects, **dict_by_projects_temp)

                    dict_by_authors = dict(dict_by_authors, **dict_by_authors_temp)

            #---------------------------------------------------------

            # projects_path = prefix + '/projects/{}/{}'.format(cur_year, cur_month)

            authors_path = '/data/Adoption_data' + '/authors/{}/{}'.format(cur_year, cur_month, )
            
            # if not os.path.exists(projects_path): os.makedirs(projects_path)

            if not os.path.exists(authors_path): os.makedirs(authors_path)

            # with open(os.path.join(projects_path, '{}.json'.format(cur_day)), 'w') as jf:

            #     json.dump(dict_by_projects, jf, indent = 4)

            with open(os.path.join(authors_path, '{}.json'.format(cur_day)), 'w') as jf:

                json.dump(dict_by_authors, jf, indent = 4)

            print('{} events are ignored...'.format(cnt))

print('all done!~!')


