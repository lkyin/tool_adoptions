# Tool Adoptions
This repository contains the data and code for [Team Discussions and Dynamics During DevOps Tool Adoptionsin OSS Projects (ASE 2020)](https://github.com/lkyin/tool_adoptions/blob/master/paper.pdf).

## Data Set
- The adoption data (i.e., GitHub Badges) is stored in `adoption_data.csv` file (under the main folder), the json version adoption data (which is much tighter) is stored in `data/tool_adoption_dict.json`.

- Comments data (with sentiment) is stored in `data/comments_with_sentiment.json file`.

- Exposure data is stored in `data/author_knowledge_dict.json`.

- Commits are stored in the `relative_sentiment_devs/merged_dict.json`.

- Github monthly events data from year 2011 to year 2018 is stored in folder `data/events`.

- Sentiment data per project is stored under folder `relative_sentiment_devs/final_combinations`.

## Sentimental Predictor
We use [Senti4SD](https://github.com/collab-uniba/Senti4SD) as for sentimental prediction. 

You need to install [Git LFS](https://git-lfs.github.com) extension to install Senti4SD locally. Once installed and initialized Git LFS, simply run:

```bash
$ git lfs clone https://github.com/collab-uniba/Senti4SD.git
```

## Replication
To reproduce the results in the paper, you can use code and data in the following specific folder.

- To obtain the curves of distribution of the adopted datas of tools and trends of various number of developers:
  - Run the jupyter file developers_trends/plot_curves.ipynb cell by cell. The jupyter file is dependent on the data in developers_trends/data folder.

- To get the relative negativity of developers: 
  - run `python relative_sentiment_devs/negativity_new_and_senior.py`, which gives the negativity of new and senior developers per month. 
  - Then run `python relative_sentiment_devs/negativity_un_exposed.py` to obtain the negativity of developers with exposure v.s. developers without exposure. 
  - Lastly, run `Rscript relative_sentiment_devs/plot_negativity.R` to generate the curve plot.

- To reproduce the relative negativity of comparable tools
  - Run `python negativity_on_categories.py`
  - Then run `Rscript plot.R` to generate the negativity plots in each tool category.

- To build our glmer models for adoption success and discussion length. 
  - Run `python glmer_model/final_table.py` to generate the aggregated final table for regressions, 
  - Then run `Rscript glmer_model/glmer_regression_models.R` to obtain the two models with R^2 scores.




