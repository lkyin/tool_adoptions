t = read.csv('/home/ylk1996/Research/CSCW1.1/results/social_dynamics_FSE.csv')

t$ratio = t$positive/(t$positive + t$negative)

t$ratio[is.nan(t$ratio)] = 0.5


adoption = t[which(t$is_adopted=='True'),]

no_adoption = t[which(t$is_adopted=='False'),]


positive_ad = length(adoption$ratio[which(adoption$ratio > 0.6)])

negative_ad = length(adoption$ratio[which(adoption$ratio < 0.4)])

neutral_ad = length(adoption$ratio[which(adoption$ratio >= 0.4 & adoption$ratio <= 0.6)])

positive_ad/(neutral_ad+negative_ad+positive_ad)

neutral_ad/(neutral_ad+negative_ad+positive_ad)

negative_ad/(neutral_ad+negative_ad+positive_ad)






positive_nad = length(no_adoption$ratio[which(no_adoption$ratio > 0.5)])

negative_nad = length(no_adoption$ratio[which(no_adoption$ratio < 0.5)])

neutral_nad = length(no_adoption$ratio[which(no_adoption$ratio >= 0.4 & no_adoption$ratio <= 0.6)])

positive_nad/(neutral_nad+negative_nad+positive_nad)

neutral_nad/(neutral_nad+negative_nad+positive_nad)

negative_nad/(neutral_nad+negative_nad+positive_nad)



