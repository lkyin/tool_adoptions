library(car)
library(stargazer)
library(lme4)
library(MuMIn)

############################### Testing ################################
df <- read.csv("final_table.csv")

# removal of outliers
rows = df$num_commits < quantile(df$num_commits, 0.98)&
       df$num_comments < quantile(df$num_comments, 0.98)&
       df$discussion_length < quantile(df$discussion_length, 0.99)&
       df$num_new_dev < quantile(df$num_new_dev, 0.99)&
       df$num_active < quantile(df$num_active, 0.99)&
       df$num_mentions < quantile(df$num_mentions, 0.99)&
       df$num_involved_dev < quantile(df$num_involved_dev, 0.99)&
       df$num_w_tool_expos < quantile(df$num_w_tool_expos, 0.99)

df = df[rows,]

####################

df$adoption_success = df$status

# aggregated table
stargazer(df[c("adoption_success","discussion_length","project_age","num_comments", "num_commits","num_new_dev",
                      "num_w_tool_expos", "num_involved_dev", "num_neg_dev", "num_pos_dev")], model.numbers = FALSE)

#######################
model.status <- glmer((status) ~ scale(discussion_length) + scale(project_age) + scale(num_mentions) + scale(num_comments) + scale(num_commits) +
                       scale(log(num_new_dev+0.1)) + scale(num_w_tool_expos) +  scale(log(num_involved_dev + 0.1))  + scale(num_pos_dev) + scale(num_neg_dev) + 
                       (1|tool), data = df, family = 'binomial',
                     glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

model.base <- glmer((status) ~ scale(discussion_length) + scale(project_age) + scale(num_mentions) + scale(num_comments) + scale(num_commits) +
                      (1|tool), data = df, family = 'binomial',
                    glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

# check vif 
vif(model.base)
vif(model.status)

# check r2
r.squaredGLMM(model.status)
r.squaredGLMM(model.base)

# generate tables
stargazer(model.base,model.status)


###################### Model Discussion Length ###############################

# full model for discussion length
model.discussion_length <- glmer(as.integer(discussion_length) ~ scale(project_age) + scale(num_mentions) + scale(num_comments) + scale(num_commits) +
                     scale(log(num_new_dev+0.1)) + scale(num_w_tool_expos) +  scale(log(num_involved_dev + 0.1))  + scale(num_pos_dev) + scale(num_neg_dev)+
                     (1|tool), data = df, family = 'poisson',
                   glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

# base model for discussion length
model.base <- glmer(as.integer(discussion_length) ~ scale(project_age) + scale(num_mentions) + scale(num_comments) + scale(num_commits) 
                      + (1|tool), data = df, family = 'poisson',
                    glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

# check vif
vif(model.discussion_length)
vif(model.base)

# check r2
r.squaredGLMM(model.base)
r.squaredGLMM(model.discussion_length)

# genereate table
stargazer(model.base, model.discussion_length)
