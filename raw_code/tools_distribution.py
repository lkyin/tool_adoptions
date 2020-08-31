import json
import pandas as pd

with open('data/tool_adoption_dict.json', 'r') as jf:

	tool_adoption_dict = json.load(jf)


tools_distribution = {}

for project in tool_adoption_dict:

	for adoption in tool_adoption_dict[project]:

		project_name, adopted_time, tool = adoption

		if tool not in tools_distribution:

			tools_distribution[tool] = []

		tools_distribution[tool].append(adopted_time)


df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in tools_distribution.items()]))

df.to_csv("data/tool_adoption_distribution.csv", sep=',')


	

	



