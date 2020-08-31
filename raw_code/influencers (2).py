import json
import datetime
from tqdm import tqdm


#--------------------Start setting the parameters----------------------

with open('data/final_project_list.txt', 'r') as f:

    project_name_list = f.readlines()

    project_name_list = [project_name.replace('\n', '') for project_name in project_name_list]

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/comments1.1/sentiment_dict.json', 'r') as jf:

    sentiment_dict = json.load(jf)

with open('/data/Adoption_data_new/comments1.1/comments_aggr_by_tool.json', 'r') as jf:

    comments_by_tool = json.load(jf)

#--------------------End setting the parameters----------------------

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


def get_heavy_influencers(project, tool):

	heavy_influencer = None

	total_comments = 0

	heavy_influencer_posts = 0

	for author in sentiment_dict[project]:

		num_posts = 0
		
		for senti, comment_date, this_tool, is_adopted in sentiment_dict[project][author]:

			if this_tool == tool:

				num_posts += 1

		total_comments += num_posts

		if num_posts > heavy_influencer_posts:

			heavy_influencer = author

			heavy_influencer_posts = num_posts

	ratio = (heavy_influencer_posts/total_comments)

	if ratio > 0.3 and heavy_influencer_posts > 5:

		print([ratio, heavy_influencer_posts])

		return heavy_influencer

	return None

def get_early_influencers(project, tool):

	# least_time = "3050-10-15T17:40:27Z"

	early_influencer = None

	if tool in comments_by_tool[project]:

		first_comment = comments_by_tool[project][tool][0]

		time, user, senti = first_comment

		#top_30_percent = 0.1 * len(comments_by_tool[project][tool])

		#for comment 

		early_influencer = user

	return early_influencer

	

def get_opinion(comments, tool):

	negs, pos = 0, 0

	for senti, comment_date, this_tool, is_adopted in comments:

		if this_tool != tool:

			continue

		if senti == 'negative':

			negs += 1

		if senti == 'positive':

			pos += 1

	if negs > pos:

		return 'negative'

	elif pos > negs:

		return 'positive' 

	else:
		return 'neutral'


influencers = {}



with open('./data/influencer.csv', 'w') as f:

	f.write('project,tool,heavy_influencer,early_influencer,hio,eio,decision\n')

	for project in project_name_list:

		#if project not in comments_by_tool:

			#return 

		influencers[project] = {}

		for tool in comments_by_tool[project]:

			#if len(comments_by_tool[project][tool]) < 5:

			#	continue

			# influencers[project][tool] = 加上类别！

			heavy_influencer = get_heavy_influencers(project, tool)

			early_influencer = get_early_influencers(project, tool)

			early_influencer_opinion = None

			heavy_influencer_opinion = None

			if early_influencer:

				comments_ei = sentiment_dict[project][early_influencer]

				early_influencer_opinion = get_opinion(comments_ei, tool)

			if heavy_influencer:

				comments_hi = sentiment_dict[project][heavy_influencer]

				heavy_influencer_opinion = get_opinion(comments_hi, tool)

			if tool in tool_adoption[project]:

				decision = 1

			else:

				decision = 0

			line_to_write = [project, tool, heavy_influencer, early_influencer, heavy_influencer_opinion, early_influencer_opinion, decision]

			line_to_write = [str(item) for item in line_to_write]

			f.write(','.join(line_to_write) + '\n')


print('all done~!!')

        






