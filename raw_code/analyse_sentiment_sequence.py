import json
import datetime

with open('result/sentiment.json', 'r') as f:

    projects = json.load(f)

with open('tool_adoption_date.json', 'r') as f:

    tool_adoption_date = json.load(f)

new_dic = {}

cnt = 0

for projectname in projects.keys():

    project = projects[projectname]

    if len(project) < 10:

        continue

    new_dic[projectname] = []

    #first_comment_date = project[0][0]
    adoption_name, tool_str = projectname.split('-', 1)

    if '-' in tool_str:
        
        tool_str = tool_str.split('-')

        tool = tool_str.pop()

        for item in tool_str:

            adoption_name = adoption_name + '-' + item

    else: tool = tool_str

    adoption_name = adoption_name.replace('__', '/')

    adoption_dates = tool_adoption_date[adoption_name]

    for this_tool, this_date in adoption_dates:

        if tool == this_tool:

            adoption_date = datetime.datetime.strptime(this_date, "%Y/%m/%d %H:%M")

    #first_comment_date = datetime.datetime.strptime(first_comment_date, "%Y-%m-%dT%H:%M:%SZ")

    for comment in project:

        try:

            date, sentiment, poster = comment

            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

            difference = (date - adoption_date).days

            if poster != 'I':

                print(poster)

            new_dic[projectname].append((difference, sentiment, poster))

        except Exception as e:

            print(e)

            continue


print(new_dic)

with open('result/difference_days_sentiment.json', 'w') as jsonfile:

    json.dump(new_dic, jsonfile)

print('all done!!')
