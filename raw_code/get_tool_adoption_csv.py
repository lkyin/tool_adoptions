import csv
from tqdm import tqdm
import json

# Convert the toll_adoption.csv file to dict file. 
# This helps us to locate the project information in an easier way

dic = {}

state_set = set()

with open('data/tool_adoption.csv','r') as myFile:

    lines = csv.reader(myFile)

    for line in tqdm(lines):

        num, project_name, time, tool, tool_type, state, series = line

        state_set.add(state)

        if project_name not in dic:

        	dic[project_name] = []

        dic[project_name].append([project_name, time, tool])


json_str = json.dumps(dic, indent=4)

with open('data/tool_adoption_dict.json', 'w') as json_file:

	json_file.write(json_str)




