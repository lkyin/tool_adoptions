import os
import json
import datetime
from tqdm import tqdm


final_combination_path = './final_combinations/'
# projects = os.listdir(final_combination_path)

with open('./project_list.txt', 'r') as f:
    projects = f.readlines()
    projects = [eval(project).replace('\n', '').replace('/', '__') for project in projects]

with open('./tool_categories.json', 'r') as jf:
	tool_categories = json.load(jf)

with open('./tool_adoption_dict.json', 'r') as jf:
	tool_adoption_dict = json.load(jf)

with open('./senti_baseline.json', 'r') as jf:
	senti_baseline = json.load(jf)

with open('./tool_belongs_cate.json', 'r') as jf:
	tool_belongs_cate = json.load(jf)


def comapre_two_date(d1, d2):

    d1 = datetime.datetime.strptime(d1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(d2, '%Y-%m-%dT%H:%M:%SZ')
    days = (d1-d2).days
    months = days/30
    return months


def generate_dict_list():
	post_sentiments = {}
	for cate in tool_categories:
		for tool1 in tool_categories[cate]:
			if tool1 not in post_sentiments:
				post_sentiments[tool1] = {}
			for tool2 in tool_categories[cate]:
				if tool2 not in post_sentiments[tool1]:
					post_sentiments[tool1][tool2] = []
	return post_sentiments

def generate_dict_dict(project_name):

	temp_post_sentiments = {}
	tools = [tool for project_name, time, tool in tool_adoption_dict[project_name]]

	for tool1 in tools:
		if tool1 not in temp_post_sentiments:
			temp_post_sentiments[tool1] = {}

		for cate in tool_categories:
			if tool1 in tool_categories[cate]:
				for tool2 in tool_categories[cate]:
					if tool2 not in temp_post_sentiments[tool1]:
						temp_post_sentiments[tool1][tool2] = {'positive':0, 'negative':0, 'neutral':0}

	return temp_post_sentiments

adoption_date_of_project = {}

for project in projects:
	project = project.replace('__', '/').replace('.txt', '')
	adoption_date_of_project[project] = {}
	for adoption in tool_adoption_dict[project]:
		project_name, time, tool = adoption
		for cate in tool_categories:
			if tool in tool_categories[cate]:
				adoption_date_of_project[project][cate] = time


# used to store all sentiments ratio before adoption
pre_sentiments = generate_dict_list()
# used to store all sentiments ratio
post_sentiments = generate_dict_list()


for project in tqdm(projects):
	with open(final_combination_path + project + '.txt', 'r') as f:
		comments = eval(f.readlines()[0])

	project = project.replace('__', '/').replace('.txt', '')

	# used to store project-specific sentiments ratio before adoption
	temp_pre_sentiments = generate_dict_dict(project)
	# used to store project-specific sentiments ratio after adoption
	temp_post_sentiments = generate_dict_dict(project)

	if project in senti_baseline:
		baseline = senti_baseline[project]
	else:continue

	with open('./result/sentiment_on_categories.csv', 'w') as csvf:
		csvf.write('project,user,comment_tool,comment_time,relative_month,sentiment\n')
		for comment in comments:

			if len(comment) == 5:
				project, user, comment_tool, comment_time, sentiment = comment

			if len(comment) == 6:
				project, user, comment_tool, comment_time, is_adopted, sentiment = comment

			for cate in tool_categories:
				if comment_tool in tool_categories[cate]:
					adoption_time = adoption_date_of_project[project][cate]
					month = comapre_two_date(comment_time, adoption_time)

			csvf.write('{},{},{},{},{},{}\n'.format(project,user,comment_tool,comment_time,month,sentiment))
			
			# pre_comment
			for adoption in tool_adoption_dict[project]:
				project_name, time, adopted_tool = adoption
				if month < 0:
					if adopted_tool in temp_pre_sentiments and comment_tool in temp_pre_sentiments[adopted_tool] and sentiment:
						temp_pre_sentiments[adopted_tool][comment_tool][sentiment] += 1

				else:
					if adopted_tool in temp_post_sentiments and comment_tool in temp_post_sentiments[adopted_tool] and sentiment:
						temp_post_sentiments[adopted_tool][comment_tool][sentiment] += 1


	for adopted_tool in temp_pre_sentiments:

		for comment_tool in temp_pre_sentiments[adopted_tool]:
			negs = temp_pre_sentiments[adopted_tool][comment_tool]['negative']
			pos = temp_pre_sentiments[adopted_tool][comment_tool]['positive']
			neus = temp_pre_sentiments[adopted_tool][comment_tool]['neutral']

			if (negs+pos) == 0:
				negativity = 0

			else:
				negativity = negs / (negs+pos)

			# relative_negativity = negativity
			relative_negativity = negativity - baseline
			pre_sentiments[adopted_tool][comment_tool].append(relative_negativity)

	# handling the post-sentiment
	for adopted_tool in temp_post_sentiments:
		for comment_tool in temp_post_sentiments[adopted_tool]:
			negs = temp_post_sentiments[adopted_tool][comment_tool]['negative']
			pos = temp_post_sentiments[adopted_tool][comment_tool]['positive']
			neus = temp_post_sentiments[adopted_tool][comment_tool]['neutral']
			if (negs+pos) == 0:
				negativity = 0
			else:
				negativity = negs / (negs+pos)

			relative_negativity = negativity - baseline
			post_sentiments[adopted_tool][comment_tool].append(relative_negativity)

with open('result.csv', 'w') as f:
	f.write('tool_pair,category,status,negativity\n')

	for adopted_tool in post_sentiments:
		for comment_tool in post_sentiments[adopted_tool]:
			lst = post_sentiments[adopted_tool][comment_tool]
			if lst:
				negativity = sum(lst)/len(lst)
			else:
				negativity = 0
			f.write('{},{},{},{}\n'.format(adopted_tool+'-'+comment_tool, tool_belongs_cate[adopted_tool], 'post', negativity))
			
	for adopted_tool in pre_sentiments:
		for comment_tool in pre_sentiments[adopted_tool]:
			lst = pre_sentiments[adopted_tool][comment_tool]
			if lst:
				negativity = sum(lst)/len(lst)
			else:
				negativity = 0
			f.write('{},{},{},{}\n'.format(adopted_tool+'-'+comment_tool, tool_belongs_cate[adopted_tool],'pre', negativity))

print('all done!!!')