import json

with open('/data/Adoption_data/commits/commits_1.json', 'r') as f:

	commits_1 = json.load(f)

print(1)

with open('/data/Adoption_data/commits/commits_2.json', 'r') as f:

	commits_2 = json.load(f)

print(2)

with open('/data/Adoption_data/commits/commits_3.json', 'r') as f:

	commits_3 = json.load(f)

print(3)

with open('/data/Adoption_data/commits/commits_4.json', 'r') as f:

	commits_4 = json.load(f)

print(4)

with open('/data/Adoption_data/commits/commits_5.json', 'r') as f:

	commits_5 = json.load(f)

print(5)


combined_dict = {**commits_1, **commits_2}

combined_dict = {**combined_dict, **commits_3}

combined_dict = {**combined_dict, **commits_4}

combined_dict = {**combined_dict, **commits_5}


with open('/data/Adoption_data/commits/merged_dict2.json', 'w') as jf:

	json.dump(combined_dict, jf)

print('all done!!!')
