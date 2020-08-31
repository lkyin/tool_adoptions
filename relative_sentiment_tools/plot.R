require(grid)
library(ggplot2)
library(viridis)

mydata <- read.csv("/data/Adoption_data_new/comments1.1/result/result.csv")

minif = mydata[which(mydata$category=='minif'),]
coverage = mydata[which(mydata$category=='coverage'),]
linter = mydata[which(mydata$category=='linter'),]
depmgr = mydata[which(mydata$category=='depmgr'),]
testing = mydata[which(mydata$category=='testing'),]

minif_p <- ggplot(minif, aes(x = tool_pair, 
                             y =negativity,
                             fill = status)) + geom_bar(stat = 'identity', colour = 'black') + coord_flip() + scale_fill_brewer(palette="Set2")  + theme(text = element_text(size=26, color = 'black'))
                                                    
minif_p

coverage_p <- ggplot(coverage, aes(x = tool_pair, 
                             y =negativity,
                             fill = status)) + geom_bar(stat = 'identity', colour = 'black') + coord_flip()+ scale_fill_brewer(palette="Set2")  + theme(text = element_text(size=26))
                             

linter_p <- ggplot(linter, aes(x = tool_pair, 
                             y =negativity,
                             fill = status)) + geom_bar(stat = 'identity', colour = 'black') + coord_flip()+ scale_fill_brewer(palette="Set2")  + theme(text = element_text(size=26)) 

depmgr_p <- ggplot(depmgr, aes(x = tool_pair, 
                             y =negativity,
                             fill = status)) + geom_bar(stat = 'identity', colour = 'black') + coord_flip()+ scale_fill_brewer(palette="Set2")  + theme(text = element_text(size=26)) 

testing_p <- ggplot(testing, aes(x = tool_pair, 
                             y =negativity,
                             fill = status)) + geom_bar(stat = 'identity', colour = 'black') + coord_flip() + scale_fill_brewer(palette="Set2")  + theme(text = element_text(size=26))

