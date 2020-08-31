#coding: utf-8

import json
import pandas as pd
import numpy


df = pd.read_csv('./data/tool_adoption.csv')

tool_name = 'mocha'

projects = df[df.tool == tool_name]

# print(projects)

projects = projects[(projects.date > '2017/1') & (projects.date < '2018/6')]

print(projects.slug)

projects.slug.to_csv('./data/case_study_projects_{}.csv'.format(tool_name), index=False)

print('all done~!')
















