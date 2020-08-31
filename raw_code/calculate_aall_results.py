import subprocess
import os

files = ['calculate_num_active.py', 'calculate_active_ratio.py', 
		'calculate_exposure.py', 'calculate_num_exposure.py',
		'calculate_involvement.py', 'calculate_num_involvement.py', 
		'calculate_sentiment.py', 'calculate_num_sentiment.py',
		'calculate_tenure.py', 'calculate_num_tenure.py']

base_command = "python3 "

for file in files:

	print('Runing {}...'.format(file))

	command = base_command + file

	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

	output, error = process.communicate()


