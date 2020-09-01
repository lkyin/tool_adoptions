import json
import os
from tqdm import tqdm
import datetime

###################################################################
path = '../relative_sentiment_tools/final_combinations/'

with open('./full_project_list.txt', 'r') as f:
    projects = f.readlines()
    project_list = [project.replace('\n', '') for project in projects]

with open('../relative_sentiment_devs/tool_adoption.json', 'r') as f:
    tool_adoption = json.load(f)

with open('../relative_sentiment_tools/tool_categories.json', 'r') as f:
    tool_categories = json.load(f)

with open('../relative_sentiment_tools/tool_belongs_cate.json', 'r') as jf:
    tool_belongs_cate = json.load(jf)

with open('../data/author_knowledge_dict.json', 'r') as jf:
    author_knowledge_dict = json.load(jf)

with open('../relative_sentiment_devs/sentiment_dict.json', 'r') as jf:
    sentiment_dict = json.load(jf)

with open('../relative_sentiment_devs/merged_dict.json', 'r') as jf:
    author_commit_histroy = json.load(jf)

with open('./project_age_dict.json', 'r') as jf:
    project_age_dict = json.load(jf)



##############################################################################

def is_exposed(author, time, tool, author_knowledge_dict):

    if (author not in author_knowledge_dict) or (tool not in author_knowledge_dict[author]):
        return False

    get_knowledge_date = author_knowledge_dict[author][tool]
    if get_knowledge_date < time:
        return True

    return False

young_threshold = 90 
def is_young_by_commit(commit_history, start_time, end_time):

    first_commit_time = commit_history[0]
    if (first_commit_time >= start_time) and (first_commit_time <= end_time):
        return True

    #gap = date_minus(first_commit_time, time)

    #if gap <= young_threshold:

    #    return True

    return False

def is_young_by_comment(comment_history, start_time, end_time):

    first_comment_time = comment_history[0][1]

    if (first_comment_time >= start_time) and (first_comment_time <= end_time):

        return True

    #gap = date_minus(first_comment_time, time)

    #if gap <= young_threshold:

    #    return True

    return False

def is_involved(project, author, tool, start_time, end_time):

    # author_sentiment_history = sentiments[project][author]

    if author in sentiment_dict[project]:

        author_sentiment_history = sentiment_dict[project][author]

    else:
        return False

    for sentiment in author_sentiment_history:

        senti, this_time, tool_name, is_this_tool = sentiment

        # if this_time < time and (tool_name == tool or tool_name == None):
        if (this_time <= end_time) and (tool_name == tool):

            return True

    return False


def get_influencer(sentiments, project, begin_date, end_date, tool):

    #input: sentiments, project, begin_date, end_date, tool
    #output: the influencers and the autitude on it

    authors = sentiments[project]

    influencer = 0

    autitude = 0

    autitude_dict = {}

    cnt = 0

    for author in authors:

        if author not in autitude_dict:

            autitude_dict[author] = []

        author_sentiment_history = authors[author]

        for sentiment in author_sentiment_history:

            senti, comment_date, tool_name, is_this_tool = sentiment

            if comment_date <= end_date and comment_date >= begin_date and tool_name == tool:

                cnt += 1

                if senti == 'negative':

                    autitude_dict[author].append(-1)

                if senti == 'positive':

                    autitude_dict[author].append(1)

    for author in autitude_dict:

        if len(autitude_dict[author]) >= 0.5 * cnt:

            influencer = 1

            autitude = sum(autitude_dict[author])

            break


    return [influencer, autitude]


def get_num_devs(all_commit_history, projects_name, start_time, end_time, this_tool):

    def did_commit(commit_history):

        for commit_date in commit_history:

            if commit_date >= start_time and commit_date <= end_time:

                return True

        return False


    def did_comment(comment_history):

        for senti, comment_date, tool, is_adopted in comment_history:

            if tool != this_tool: continue

            if comment_date >= start_time and comment_date <= end_time:

                return True

        return False

    committer = set()

    active_devs = set()

    exposed_devs = set()

    young_devs_by_commit = set()

    young_devs_by_comment = set()

    involved_devs = set()

    commiting_authors = all_commit_history[projects_name]

    # adding devs by commiting behaviors
    for author in commiting_authors:

        commit_history = commiting_authors[author][:]
        
        if did_commit(commit_history): 

            active_devs.add(author)

            committer.add(author)

            # involved_devs.add(author)


    # adding devs by commenting behaviors
    commenting_authors = sentiment_dict[projects_name]

    for author in commenting_authors:

        comment_history = commenting_authors[author][:]
        
        if did_comment(comment_history): 

            active_devs.add(author)

            involved_devs.add(author)

    for active_dev in active_devs:

        if is_exposed(active_dev, end_time, this_tool, author_knowledge_dict):

            exposed_devs.add(active_dev)

        if active_dev in all_commit_history[projects_name]:

            commit_history = all_commit_history[projects_name][active_dev]

            if is_young_by_commit(commit_history, start_time, end_time):

                young_devs_by_commit.add(active_dev)

        # if this active_dev comment 
        if projects_name in sentiment_dict and active_dev in sentiment_dict[projects_name]:

            comment_history = sentiment_dict[projects_name][active_dev]

            if is_young_by_comment(comment_history, start_time, end_time):

                young_devs_by_comment.add(active_dev)

            #if is_involved(projects_name, active_dev, this_tool, start_time, end_time):

            #    involved_devs.add(active_dev)

    pos, neg = get_emotional_devs(projects_name, active_devs, this_tool, start_time, end_time)

    return [active_devs, exposed_devs, young_devs_by_commit, young_devs_by_comment, involved_devs, committer, pos, neg]


def get_number_mentions(sentiments, project, begin_date, end_date, tool):

    #input: projects_url, time
    #output: the list of negative developers

    authors = sentiments[project]

    num_mentions = 0

    for author in authors:

        author_sentiment_history = authors[author]

        for sentiment in author_sentiment_history:

            senti, comment_date, tool_name, is_this_tool = sentiment

            if comment_date <= end_date and comment_date >= begin_date and tool_name == tool:

                num_mentions += 1

    return num_mentions

def get_number_comments(sentiments, project, begin_date, end_date, tool):

    #input: projects_url, time
    #output: the list of negative developers

    authors = sentiments[project]

    num_negative_comments = 0

    num_neutral_comments = 0

    num_positive_comments = 0

    for author in authors:

        author_sentiment_history = authors[author]

        for sentiment in author_sentiment_history:

            senti, comment_date, tool_name, is_this_tool = sentiment

            if comment_date <= end_date and comment_date >= begin_date:

                # print(begin_date, comment_date, end_date, tool_name, tool)

                if senti == 'negative':

                    num_negative_comments += 1

                if senti == 'positive':

                    num_positive_comments += 1

                if senti == 'neutral':

                    num_neutral_comments += 1

    num_comments = sum([num_positive_comments, num_neutral_comments, num_negative_comments])

    return [num_comments, num_positive_comments, num_neutral_comments, num_negative_comments]

def get_num_commits(all_commit_history, projects_name, start_time, end_time):

    #input: projects_url, time
    #output: the list of active developers

    num_of_commits = 0

    authors = all_commit_history[projects_name]

    for author in authors:

        commit_history = authors[author][:]

        commit_history = commit_history[:]

        # commit_history.sort()

        for commit_date in commit_history:

            if commit_date >= start_time and commit_date <= end_time:

                num_of_commits += 1

    return num_of_commits


def get_emotional_devs(project, devs, tool, start_time, end_time):

    # author_sentiment_history = sentiments[project][author]

    devs_dict = {}

    for author in devs:

        if author not in sentiment_dict[project]:

            continue

        devs_dict[author] = 0

        author_sentiment_history = sentiment_dict[project][author][:]

        for sentiment in author_sentiment_history:

            senti, this_time, tool_name, is_this_tool = sentiment

            senti = senti.replace('\r', '')

            if (tool_name == tool) and (this_time >= start_time and this_time <= end_time):
            # if (tool_name == tool or tool_name == 'None') and (this_time >= start_time and this_time <= end_time):

                if senti == 'negative':

                    devs_dict[author] -= 1

                if senti == 'positive':

                    devs_dict[author] += 1
    
    neg = set()

    pos = set()

    for author in devs_dict:

        if devs_dict[author] > 0:

            pos.add(author)

        if devs_dict[author] < 0:

            neg.add(author)


    return [pos, neg]

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


def get_start_time(project_name, tool):

    # path = '../relative_sentiment_tools/final_combinations/'

    project_name = project_name.replace('/', '__')

    if not os.path.exists(path + project_name + '.txt'):

        # print('not existing....')

        return None

    with open(path + project_name + '.txt', 'r') as f:

        comments = eval(f.readlines()[0])

    for comment in comments:
        
        try:

            project_name, user, this_tool, comment_time, is_adopted, sentiment = comment

        except:

            project_name, user, this_tool, comment_time, is_adopted = comment

        if this_tool == tool:

            return comment_time

    return None


def get_end_time(project_name, tool, end_time):

    # path = '../relative_sentiment_tools/final_combinations/'

    project_name = project_name.replace('/', '__')

    if not os.path.exists(path + project_name + '.txt'):

        return None

    with open(path + project_name + '.txt', 'r') as f:

        comments = eval(f.readlines()[0])

    for comment in comments[::-1]:

        # comment = ['webtorrent/parse-torrent-file', 'rom1504', 'sauce', '2016-03-16T15:23:48Z', True, 'neutral']
        #           ['behance/lightbox', 'designjockey', 'karma', '2016-09-22T15:38:41Z', False]
        try:

            project_name, user, this_tool, comment_time, is_adopted, sentiment = comment

        except:

            project_name, user, this_tool, comment_time, is_adopted = comment

        # print([comment_time, end_time])

        if this_tool == tool and comment_time <= end_time:

            return comment_time

    return None


with open('test.csv', 'w') as f:

    f.write('project,tool,discussion_length,project_age,time_to_adoption,num_new_dev,num_w_tool_expos,num_active,num_involved_dev,num_committers,num_commits,num_neg_dev,num_pos_dev,num_comments,num_neutral_comments,num_positive_comments,num_negative_comments,num_mentions,influ,influ_at,adoption_success\n')

    print(len(project_list))

    for project in tqdm(project_list):

        studied_cate = set()

        tools = sorted(list(tool_adoption[project]))

        for tool in tools:

            this_cate = tool_belongs_cate[tool]

            adoption_time = tool_adoption[project][tool]

            project_age = project_age_dict[project][tool] / 30

            if this_cate in studied_cate:

                continue

            studied_cate.add(this_cate)

            for pc_tool in tool_categories[this_cate]:

                # not counted since standard can be used in not a tool context
                if pc_tool == 'standard':
                    continue

                start_time = get_start_time(project, pc_tool)

                end_time = adoption_time

                # set the last comment to be the end time

                last_comment_time = get_end_time(project, pc_tool, adoption_time)

                # end_time = last_comment_time
                
                # if there is no comment on that tool
                if (not end_time) or (not start_time) or (date_minus(start_time, end_time) <= 0):

                    continue

                    if pc_tool in tool_adoption[project]: 

                        status = 1

                    # did not adopt is 0
                    else:

                        continue

                        status = 0

                    result = [project,pc_tool,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,None,None,status]

                    str_result = [str(r) for r in result]

                    f.write(','.join(str_result) + '\n')

                    continue

                # print([last_comment_time, adoption_time])

                delivery_length = (date_minus(start_time, end_time)) /30

                time_to_adoption = date_minus(last_comment_time, adoption_time) / 30

                num_mentions = get_number_mentions(sentiment_dict, project, start_time, end_time, pc_tool)
                
                num_comments, num_positive_comments, num_neutral_comments, num_negative_comments = get_number_comments(sentiment_dict, project, start_time, end_time, pc_tool)

                influ, influ_at = get_influencer(sentiment_dict, project, start_time, end_time, pc_tool)

                num_commits = get_num_commits(author_commit_histroy, project, start_time, end_time)

                active_devs, exposed_devs, young_devs_by_commit, young_devs_by_comment, involved_devs, num_committers, pos, neg = get_num_devs(author_commit_histroy, project, start_time, end_time, pc_tool)

                num_positive_devs, num_negative_devs = len(pos), len(neg)

                num_active, num_new, num_involved, num_exposed = len(active_devs), len(young_devs_by_commit.union(young_devs_by_comment)), len(involved_devs), len(exposed_devs)

                num_committers = len(num_committers)
                # adopted is 1
                if pc_tool in tool_adoption[project]: status = 1

                # did not adopt is 0
                else: status = 0

                result = [project,pc_tool,delivery_length,project_age,time_to_adoption,num_new,num_exposed,
                num_active,num_involved,num_committers,num_commits,num_negative_devs, num_positive_devs, 
                num_comments,num_neutral_comments,num_positive_comments,num_negative_comments,num_mentions,influ,influ_at,status]


                str_result = [str(r) for r in result]

                f.write(','.join(str_result) + '\n')

print('all done~!')































