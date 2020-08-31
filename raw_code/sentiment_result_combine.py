import json
import datetime
import os



with open('/data/Adoption_data_new/comments/index.txt', 'r') as f:

    sentiment_index = eval(f.readlines()[0])

with open('/data/Adoption_data_new/comments/result_final.csv', 'r') as csvf:

    lines = csvf.readlines()

print(len(sentiment_index), len(lines))

# ['MaxMEllon/comelon', 'MaxMEllon', 'eslint', '2016-03-12T09:02:13Z', False]

for i in range(len(sentiment_index)):

    line = lines[i].replace('\n', '')

    row, sentiment = line.split(',')

    sentiment_index[i].append(sentiment)

    #print(sentiment_index[i])


project_sentiment_dict = {}


for comment in sentiment_index:
	
	project_name, author, tool_name, time, is_adopted, sentiment = comment

	if project_name not in project_sentiment_dict:

		project_sentiment_dict[project_name] = {}

	if author not in project_sentiment_dict[project_name]:

		project_sentiment_dict[project_name][author] = []

	project_sentiment_dict[project_name][author].append([sentiment, time, tool_name, is_adopted])


with open('/data/Adoption_data_new/comments/sentiment_dict.json', 'w') as jf:

	json.dump(project_sentiment_dict, jf, indent = 4)

print('so great, so good.')

