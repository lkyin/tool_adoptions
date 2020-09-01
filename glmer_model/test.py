import os

with open('./test.csv', 'r') as f:
	lines = f.readlines()

projects = []
for line in lines:
	project_name, *rest = line.split(',')
	projects.append(project_name)

with open('test_projects2.txt', 'w') as f:
	for p in projects[1:]:
		f.write('{}\n'.format(p))


