import pandas as pd

#df = pd.read_csv('result.csv')

with open('result.csv', 'r') as csvf:
	lines = csvf.readlines()
	
pre = {}
post = {}

for line in lines[1:]:
	adopted_tool,comment_tool,status,negativity = line.split(',')
	negativity = negativity.replace('\n','')

	if status == 'pre':
		if adopted_tool not in pre:
			pre[adopted_tool] = {}
		pre[adopted_tool][comment_tool] = negativity

	if status == 'post':
		if adopted_tool not in post:
			post[adopted_tool] = {}
		post[adopted_tool][comment_tool] = negativity

pre_df = pd.DataFrame.from_dict(pre)
post_df = pd.DataFrame.from_dict(post)

pre_df.to_csv('pre_table.csv')
post_df.to_csv('post_table.csv')

print('all done~!~')