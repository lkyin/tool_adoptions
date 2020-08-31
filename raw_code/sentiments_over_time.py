import json
import datetime
from tqdm import tqdm
from math import floor

#--------------------Start setting the parameters----------------------

with open('/home/ylk1996/Research/CSCW1.1/data/tool_adoption.json', 'r') as f:

    tool_adoption = json.load(f)

with open('/data/Adoption_data_new/comments1.1/comments_by_tool_relative_time.json', 'r') as jf:

    comments_by_tool = json.load(jf)

#--------------------End setting the parameters----------------------

def date_minus(date1, date2):
    
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    
    days = (d2 - d1).days

    return days


ad = {'negative':[], 'positive':[], 'neutral':[]}

non_ad = {'negative':[], 'positive':[], 'neutral':[]}

for project in comments_by_tool:

	for tool in comments_by_tool[project]:

		if tool in tool_adoption[project]:

			is_adopted = True

		else:

			is_adopted = False

		for comment in comments_by_tool[project][tool]:

			relative_days, user, senti = comment

			relative_month = relative_days/ 30

			if relative_month < -12 or relative_month > 12:

				continue

			if is_adopted:

				ad[senti].append(relative_month)

			else:

				non_ad[senti].append(relative_month)


for senti in ad:

	ad[senti].sort()

	non_ad[senti].sort()



rst_ad = {'negative': [0]*24, 'positive': [0]*24, 'neutral': [0]*24}

rst_non_ad = {'negative': [0]*24, 'positive': [0]*24, 'neutral': [0]*24}

monthly = list(range(-12,12))

for senti in ad:

	for time in ad[senti]:

		this_time = floor(time) + 11

		rst_ad[senti][this_time] += 1



for senti in non_ad:

	for time in non_ad[senti]:

		this_time = floor(time) + 11

		#if this_time not in rst_non_ad[senti]:

		#	rst_non_ad[senti][this_time] = 0

		# print(this_time)
			
		rst_non_ad[senti][this_time] += 1


print(rst_ad)

print('#########################################')

print(rst_non_ad)

with open('./data/sentiment_overtime_adopted.json', 'w') as jf:

	json.dump(rst_ad, jf, indent = 4)

with open('./data/sentiment_overtime_non_adopted.json', 'w') as jf:

	json.dump(rst_non_ad, jf, indent= 4)

print('all done~!!')

        






