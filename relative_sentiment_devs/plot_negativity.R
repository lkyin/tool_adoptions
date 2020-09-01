# senior and new

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

df1 <- read.csv("./negativity_new_senior.csv")

ggplot(df1, aes(x=month, y=num, group=group)) +
  geom_line(aes(color=group),linetype = "dashed", size = 0.8)+
  geom_point(aes(color=group),shape=0)+
  theme(legend.title = element_text(size=18), legend.text = element_text(size=18), legend.position = c(0.1, 0.80))+
  theme(axis.text.x = element_text(color = "grey20", size = 18, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 18, face = "plain"),  
        axis.title.x = element_text(color = "grey20", size = 18, face = "plain"),
        axis.title.y = element_text(color = "grey20", size = 15, face = "plain"))+
  xlab("Relative months to Adoption") + ylab("Per Dev Neg Comments")+
  +theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))

ggsave('./negativity_new_c.pdf', device = "pdf")

##################### Exposure #############

df2 <- read.csv("./negativity_exposure.csv")

ggplot(df2, aes(x=month, y=num, group=group)) +
  geom_line(aes(color=group),linetype = "dashed",size = 0.8)+
  geom_point(aes(color=group),shape=0)+
  theme(legend.title = element_text(size=18), legend.text = element_text(size=18), legend.position = c(0.2, 0.80))+
  theme(axis.text.x = element_text(color = "grey20", size = 18, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 18, face = "plain"),  
        axis.title.x = element_text(color = "grey20", size = 18, face = "plain"),
        axis.title.y = element_text(color = "grey20", size = 15, face = "plain"))+
  xlab("Relative months to Adoption") + ylab("Per Dev Neg Comments") +
  +theme(plot.margin=grid::unit(c(0,0,0,0), "mm"))

ggsave('./negativity_exposed_c.pdf', device = "pdf")






