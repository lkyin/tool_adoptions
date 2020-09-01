require(grid)
library(ggplot2)
library(viridis)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

mydata <- read.csv("/data/adoption_data_final/tool_adoptions/relative_sentiment_tools/result.csv")

minif = mydata[which(mydata$category=='minif'),]
coverage = mydata[which(mydata$category=='coverage'),]
linter = mydata[which(mydata$category=='linter'),]
depmgr = mydata[which(mydata$category=='depmgr'),]
testing = mydata[which(mydata$category=='testing'),]


# testing
ggplot(testing, aes(x = tool_pair, 
  y =negativity, fill = status)) + 
  geom_bar(stat = 'identity', colour = 'black') + 
  coord_flip() + 
  scale_fill_brewer(palette="Set2")  + 
  theme(text = element_text(size=16)) +
  theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))+
  xlab("Compared Tools") + ylab("Relative Negativity")

ggsave('./testing_p.pdf', device = "pdf")


# linter
ggplot(linter, aes(x = tool_pair, 
                   y =negativity, fill = status)) + 
  geom_bar(stat = 'identity', colour = 'black') + 
  coord_flip() + 
  scale_fill_brewer(palette="Set2")  + 
  theme(text = element_text(size=16)) +
  theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))+
  xlab("Compared Tools") + ylab("Relative Negativity")

ggsave('./linter_p.pdf', device = "pdf")


# minif
ggplot(minif, aes(x = tool_pair, 
                     y =negativity, fill = status)) + 
  geom_bar(stat = 'identity', colour = 'black') + 
  coord_flip() + 
  scale_fill_brewer(palette="Set2")  + 
  theme(text = element_text(size=16)) +
  theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))+
  xlab("Compared Tools") + ylab("Relative Negativity")


# coverage
ggplot(coverage, aes(x = tool_pair, 
                    y =negativity, fill = status)) + 
  geom_bar(stat = 'identity', colour = 'black') + 
  coord_flip() + 
  scale_fill_brewer(palette="Set2")  + 
  theme(text = element_text(size=16)) +
  theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))+
  xlab("Compared Tools") + ylab("Relative Negativity")



##depmgr
ggplot(depmgr, aes(x = tool_pair, 
  y =negativity, fill = status)) + 
  geom_bar(stat = 'identity', colour = 'black') + 
  coord_flip() + 
  scale_fill_brewer(palette="Set2")  + 
  theme(text = element_text(size=16)) +
  theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))+
  xlab("Compared Tools") + ylab("Relative Negativity")



