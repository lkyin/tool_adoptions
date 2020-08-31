#coding: utf-8

"""
Created on Mon Mar 12 15:19:52 2019

@author: Likang Yin

"""

import requests
import datetime
import json
import pandas as pd
import numpy
import math
import copy
import random
import csv
import codecs
import re
import concurrent.futures
from get_login import get_login
from tqdm import tqdm


############################################################################################################################################
#--------------------Start setting the parameters----------------------

with open('data/case_study_projects_mocha.csv', 'r') as f:

    project_name_list = f.readlines()

    project_name_list = [project_name.strip('\n') for project_name in project_name_list]

with open('data/tool_adoption_dict.json', 'r') as f:

    tool_adoption_dict = json.load(f)


#--------------------End setting the parameters----------------------
############################################################################################################################################



def contain_non_English(check_str):
    '''
    # This function checks whether the comment is written in non-English..
    # Input: a comment (string)
    # RETURN: a boolean value
    '''

    for ch in check_str:

        if u'\u4e00' <= ch <= u'\u9fff':

            return True # it contains non-English words.

    return False # it does not contain non-English words.


def refine_text(body):

    # remove emojis...
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)    

    # remove all the \ts, \ns, and blanks.
    body = body.replace('\n','').replace('\t','').replace('\r','').replace('@', '').replace(',', '.')

    # remove all the 'http' urls from the comments.
    body = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', body) 

    # make all comments are in lower case.
    body = body.lower() 

    # remove all the emojis from the comment
    body = emoji_pattern.sub(r'', body)

    # remove the blank before and after the string
    body = body.strip()

    return body

def check_valid(body, adopted_tool_list, is_valid=False):

    is_adopted = False

    this_tool = None # this comment should contain this tool name

    for test_tool in tool_list:

        if test_tool in body: 

            if test_tool in adopted_tool_list:

                is_adopted = True

            is_valid = True

            this_tool = test_tool # ah, this comment contains the tool that we want

            break

    if not is_valid: return [False, is_adopted, this_tool]

    if body[0] == '[' or body[0] == '!': return [False, is_adopted, this_tool]

    if body.count('/') > 3 or body.count('=') > 3: return [False, is_adopted, this_tool]

    # remove automatically generated comments by tools...
    dumps = ['fixed', '1.', '2.', '3.', '4.', '5.', '6.','7.','8.','9.','0.', '[codacy]', 'version', '[snyk', '[snyk update]', '[![', 'just got published.', '[Current coverage]', '[Update to this version instead', '[Coverage Status]', '[Codecov]', '[View Details]', '[Impacted file tree graph]', 'your tests are passing again.']

    is_dump = False

    for dump in dumps:

        # if those are dumps...
        if dump in body: 

            is_dump = True

            break

    # if this comment/issue contains useless messages.       
    if is_dump: return [False, is_adopted, this_tool]

    # if this comment/issue contain any non-english words, we will pass it (because it cannot be untokenized).
    if contain_non_English(body): return [False, is_adopted, this_tool]

    return [True, is_adopted, this_tool]

def process_comments(comments, project_name, adopted_tool_list, from_issue = False):

    '''
    # this function checks whether the comment is written in non-English..
    # input: all the comments (string), and the Tool Adoption Day (TAD), and the type of inquiries ('comment' or 'issue').
    # RETURN: None. Directly add comments to rst_comments which is our final data structure.

    '''

    rst_comments = []

    for comment in comments:

        body = comment['body']

        if not body: continue

        created_date = comment['created_at']

        this_author = comment['user']['login']

        # ------------------------------ process the text-------------------------------------#

        # if this comment does not contain any tool name, we will drop it.

        isvalid, is_adopted, this_tool = check_valid(body, adopted_tool_list, from_issue)

        if isvalid == False: continue

        body = refine_text(body)

        # --------------------------------- End processing the text-------------------------------------#
        
        rst_comments.append([body, created_date, this_author, is_adopted, this_tool])

    return rst_comments

def process_issues(issues, project_name, adopted_tool_list):

    '''
    # this function checks whether the comment is written in non-English..
    # input: all the comments (string), and the Tool Adoption Day (TAD), and the type of inquiries ('comment' or 'issue').
    # RETURN: None. Directly add comments to rst_comments which is our final data structure.

    '''

    rst_comments = []

    for issue in issues:

        # combine both issue title and body
        title = issue['title']

        body = issue['body']

        if title and body:

            body = issue['title'] + '. ' + issue['body']

        else:

            body = issue['title'] or issue['body']

        if not body: continue

        created_date = issue['created_at']

        this_author = issue['user']['login']


        # ------------------------------ process the issue-------------------------------------#

        # if this comment does not contain any tool name, we will drop it.

        isvalid, is_adopted, this_tool = check_valid(body, adopted_tool_list)

        if not isvalid: continue

        body = refine_text(body)

        rst_comments.append([body, created_date, this_author, is_adopted, this_tool])

       
    return rst_comments

def get_comments(project_name, adopted_tool_list):

    '''
    This function used to gather all comments on issues.

    '''

    rst_comments = []

    per_page = 100

    comments_url = 'https://api.github.com/repos/{}/issues/comments?per_page={}'.format(project_name, per_page)

    r = requests.get(comments_url, headers=headers, auth=random.choice(auth_set))

    if not r.ok:

        print(r, project_name)

    else:

        pages_cnt = 1

        comments_of_this_page = json.loads(r.text or r.content)

        try:

            rst_comments += process_comments(comments_of_this_page, project_name, adopted_tool_list)

        except:

            pass

        while 'next' in r.links.keys():

            pages_cnt += 1

            r = requests.get(r.links['next']['url'], headers=headers, auth=random.choice(auth_set))

            if not r.ok:

                continue

            else:

                comments_of_this_page = json.loads(r.text or r.content)

                try:

                    rst_comments += process_comments(comments_of_this_page, project_name, adopted_tool_list)

                except:

                    pass

        print('processed {} comments'.format(pages_cnt*per_page))

    return rst_comments

def get_issues(project_name, adopted_tool_list):

    # processing the issues (including pull requests)

    rst_comments = []

    com_tpye = 'issue'

    per_page = 100

    issues_url = 'https://api.github.com/repos/{}/issues?state={}&per_page={}'.format(project_name, 'all', per_page)

    r = requests.get(issues_url, headers=headers, auth=random.choice(auth_set))

    if not r.ok:

        print(r, project_name)

    else:

        pages_cnt = 1

        issues_of_this_page = json.loads(r.text or r.content)

        rst_comments += process_issues(issues_of_this_page, project_name, adopted_tool_list)

        while 'next' in r.links.keys():

            pages_cnt += 1

            r = requests.get(r.links['next']['url'], headers=headers, auth=random.choice(auth_set))

            if not r.ok:

                continue

            else:

                issues_of_this_page = json.loads(r.text or r.content)

                rst_comments += process_issues(issues_of_this_page, project_name, adopted_tool_list)

        print('processed {} issues'.format(pages_cnt * per_page))

    return rst_comments

def write_comments_to_file(comments, project_name):

    if len(comments) == 0:

        return None

    #print(comments)
    # ['blueseph/amuse', 'blueseph', 'istanbul', '2017-02-07T06:17:12Z', True, 'add test coverage via istanbul']

    project_name = project_name.replace('/', '__')

    filename = './data/casestudy/{}/{}.csv'.format(tool_list[0], project_name)

    with open(filename, 'w', encoding="utf-8") as f:

        f.write('project_name,user,tool,time,is_adopted,comment\n')

        for comment in comments:

            project_name, user, tool, time, is_adopted, comment_body = comment

            # if this comment is not the last comment

            comment_body = comment_body.replace('\n','').replace('\t','').replace('\r','')

            f.write('{},{},{},{},{},{}\n'.format(project_name, user, tool, time, is_adopted, comment_body))

    return None


def main(project_name):
# this main function is used to perform multithreading

    rst_comments_index = []

    # comment_set is used to check whether there are some same comments at the same time..
    comment_set = set()

    # get the adopted tool list for that project name
    adopted_tool_list = [adopted_tool for projects_n, adoption_date, adopted_tool in tool_adoption_dict[project_name]]

    # return comments on issues
    # comments = get_comments(project_name, adopted_tool_list)

    # return the title + body issues 
    issues = get_issues(project_name, adopted_tool_list)

    # merge the comments and issues
    combined_comments = issues

    # sort the combined comments by created date....
    combined_comments = sorted(combined_comments, key=lambda combined_comments: combined_comments[1])

    # store all the comments into a dict, and output all of the comments to a single file.
    # in order to find the corresponding comments, we need to establish a index 
    
    num_of_same_comments = 0

    for comment_body, created_date, this_author, is_adopted, this_tool in combined_comments:

        if comment_body not in comment_set:

            comment_set.add(comment_body)

            rst_comments_index.append([project_name, this_author, this_tool, created_date, is_adopted, comment_body])

        else:

            num_of_same_comments += 1

    # print('There are {} comments are the same'.format(num_of_same_comments))

    return [rst_comments_index, project_name]

#-----------------------------------------------------------------------

print ("Start loading...")

#with open("author_commits_date.json", "r") as file:

#    author_commits = json.load(file)


tool_set = set()

project_name_list = project_name_list[:]

# only include the tools in the project that we are interested in
for project in project_name_list:

    for adoption in tool_adoption_dict[project]:

        project_name, time, tool_name = adoption

        tool_set.add(tool_name)

tool_list = ['mocha']

#find out all the tool names. and make sure that they are included in all the comments.


#--------------------Start setting the parameters----------------------

project_id = 0

project_comments = {}

# this is used to store all the comments and output them into only one csv file
comments_index = []

auth_set = get_login()

headers = {'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

#--------------------End setting the parameters----------------------

print('Processing the data...')

total_number_of_projects = len(project_name_list)

# this dict is used to look up comment related information (e.g., created date, comment type) for later usage...
# rst_dict = {}

with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:

    for rst_comments_index, project_name in executor.map(main, project_name_list):

        project_id += 1

        print('there are {} projects left'.format(total_number_of_projects - project_id))

        ## comments_index += rst_comments_index

        write_comments_to_file(rst_comments_index, project_name)

##write_comments_to_file(comments_index)

print ('All Done!!!')
