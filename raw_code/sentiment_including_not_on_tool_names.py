#coding: utf-8

import subprocess
import os

############################################################################################################################################
#--------------------Start setting the parameters----------------------

path = '/data/Adoption_data_new/comments/including_not_tool_name/comments/'

dirs = os.listdir(path)

#--------------------End setting the parameters----------------------
############################################################################################################################################

for filename in dirs:

	file_path = path + filename

	bash_command = "sh /data/Adoption_data_new/Senti4SD/ClassificationTask/classificationTask.sh"

	result_path = './test/' + filename

	r = '/data/Adoption_data_new/Senti4SD/ClassificationTask/csvs/'

	#if os.path.exists(r+filename):

	#	print('YES')

	#	continue

	command = bash_command + ' ' + file_path + ' ' + result_path

	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

	output, error = process.communicate()




print ('All Done!!!')
