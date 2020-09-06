# Tool Adoptions
This repository contains the data and code for [Team Discussions and Dynamics During DevOps Tool Adoptionsin OSS Projects] (https://github.com/lkyin/tool_adoptions/blob/master/paper.pdf) (ASE 2020).

## Data set
1. The adoption data (i.e., GitHub Badges) is stored in adoption_data.csv file (under the main folder), the json version adoption data (which is much tighter) is stored in data/tool_adoption_dict.json.

2. Comments data (with sentiment) is stored in data/comments_with_sentiment.json file.

3. Exposure data is stored in author_knowledge_dict.json.

4. Commits are stored in the relative_sentiment_devs/merged_dict.json.

5. Github monthly events data from year 2011 to year 2018 is stored in folder data/events.

6. Sentiment data per project is stored under folder relative_sentiment_devs/final_combinations.

## Replication
To reproduce the results in the paper, you can use code and data in the following specific folder.

1. To obtain the curves of various number of developers, run the jupyter file developers_trends/plot_curves.ipynb cell by cell. The jupyter file is dependent on the data in developers_trends/data folder.

2. To get the relative negativity of developers: run relative_sentiment_devs/negativity_new_and_senior.py, which gives the negativity of new and senior developers per month. Then run relative_sentiment_devs/negativity_un_exposed.py to obtain the negativity of developers with exposure v.s. developers without exposure. Then run relative_sentiment_devs/plot_negativity.R to generate the curve plot.

3. To reproduce the relative negativity of comparable tools: run negativity_on_categories.py, then run plot.R to generate the negativity plots in each tool category.

4. To build our glmer models for adoption_success and discussion_length. Run glmer_model/final_table.py to generate the aggregated final table for regressions, then run glmer_model/glmer_regression_models.R to obtain the two models with R2 scores.




