# Tool Adoptions
This repository contains the data and code for [Team Discussions and Dynamics During DevOps Tool Adoptionsin OSS Projects] (https://github.com/lkyin/tool_adoptions/blob/master/paper.pdf) (ASE 2020).

## Data set
The adoption data (i.e., GitHub Badges) is stored in adoption_data.csv file.
The raw commit data and comments data (with sentiment) of the projects is located in data file.
The Github monthly events data of the selected projects from year 2011 to year 2018 is stored in folder data/events.
The exposure data of developers is stored in author_knowledge_dict.json.

## Replication
To reproduce the results in the paper, you can use code and data in the specific folder.
For example, if you want to reproduce our glmer model for both adoption status and discussion length, use the glmer_regression_models.R in glmer_model folder.
Since the code is written in R, you will need R compiler to run the regressions.

Will add more documentation of code in raw_code folder.



