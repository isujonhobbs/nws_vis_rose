library(ggplot2)
library(reshape2)
library(plyr)
library(colorspace)

source("mosaicfns.R")

theme_mat = theme_bw() 
theme_mat$axis.title.x$size = 14
theme_mat$axis.text.x$size = 12
theme_mat$axis.title.y$size = 14
theme_mat$axis.text.y$size = 12
theme_mat$plot.title$size = 16
theme_mat$plot.title$hjust = 0.5
theme_mat$legend.position = "right"
theme_mat$legend.text$size = 10
theme_mat$legend.title$size = 12
theme_mat$strip.text$size = 12

vstmp = read.csv("Vis_Temp.csv")
vstmp$VisFact = factor(vstmp$Vis)

g1 = ggplot(vstmp,aes(x=VisFact,y=Td.Tw)) + geom_boxplot() + 
     xlab("Visibility") + ylab("Td - Tw") + theme_mat +  

pdf("TempVis.pdf",width=8,height=6)
print(g1)
dev.off()

# Mosaic
#xfrm = as.data.frame(xvl)
#names(xfrm) = xnms
xgrplb = c("< -5","[-5,-2)","[-2,-1)","[-1,0)","[0,1)","[1,2)","[2,3)","[3,5]","> 5")
vstmp$TempCat = 1
vstmp$TempCat[vstmp$Td.Tw >= -5 & vstmp$Td.Tw < -2] = 2
vstmp$TempCat[vstmp$Td.Tw >= -2 & vstmp$Td.Tw < -1] = 3
vstmp$TempCat[vstmp$Td.Tw >= -1 & vstmp$Td.Tw < 0] = 4
vstmp$TempCat[vstmp$Td.Tw >= 0 & vstmp$Td.Tw < 1] = 5
vstmp$TempCat[vstmp$Td.Tw >= 1 & vstmp$Td.Tw < 2] = 6
vstmp$TempCat[vstmp$Td.Tw >= 2 & vstmp$Td.Tw < 3] = 7
vstmp$TempCat[vstmp$Td.Tw >= 3 & vstmp$Td.Tw <= 5] = 8
vstmp$TempCat[vstmp$Td.Tw > 5] = 9

mscdat = mosaicdat(vstmp,xvar="TempCat",yvar="VisFact")
vismrg = mrgdat(vstmp,xvar="TempCat")

g13 = sequential_hcl(13,h=15,c.=c(80,0),l=c(30,80),power=1.0)
# Plot
gmsc = ggplot(mscdat,aes(ymin=ymin,ymax=ymax,xmin=CumMin,xmax=CumMarg)) + 
       geom_rect(aes(fill=VisFact),colour="#FFFFFF") + 
       scale_fill_manual("Visibility",values=g13) +
       geom_text(aes(x=CumAvg,y=1.03,label=xgrplb,
                ymin=NULL,ymax=NULL,xmin=NULL,xmax=NULL,fill=NULL),
                data=vismrg,size=4) + 
       scale_x_continuous("Td - Tw",breaks=seq(0,1,by=0.2)) +
       ylab("Visibility") + 
       ggtitle("Visibility vs Td-Tw") + theme_mat
pdf("Vis_Temp_Mosaic.pdf",width=10,height=8)
print(gmsc)
dev.off()



