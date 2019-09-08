# Summarize practice distributions and compare to the "tobit" model

library(reshape2)
library(plyr)
library(ggplot2)

srtprbs = function(dfrm,var2) {
    # Reorder
    dsrt = dfrm[order(dfrm[,var2]),]
    dsrt$ymax = cumsum(dsrt$Cond)
    dsrt$ymin = dsrt$ymax - dsrt$Cond
    return(dsrt)
}

mosaicdat = function(dfrm,xvar,yvar) {
    # Output a data frame with rectangles suitable for mosaic plot
    jnttbl = as.data.frame(table(dfrm[,xvar],dfrm[,yvar]) / nrow(dfrm) )
    names(jnttbl) = c(xvar,yvar,"Joint")
    mrgtbl = as.data.frame(table(dfrm[,xvar]) / nrow(dfrm) )
    names(mrgtbl) = c(xvar,"Marg")
    mrgtbl$CumMarg = cumsum(mrgtbl$Marg)
    mrgtbl$CumMin = mrgtbl$CumMarg - mrgtbl$Marg
    mrgtbl$CumAvg = (mrgtbl$CumMarg + mrgtbl$CumMin) / 2
    jprbs = merge(jnttbl,mrgtbl)
    jprbs$Cond = jprbs$Joint / jprbs$Marg
    jprb2 = ddply(jprbs,c(xvar),.fun=srtprbs,var2=yvar)
    return(jprb2)
}

mrgdat = function(dfrm,xvar) {
    # Output data frame with marginal probabilities for x component
    # of mosaic plot
    mrgtbl = as.data.frame(table(dfrm[,xvar]) / nrow(dfrm) )
    names(mrgtbl) = c(xvar,"Marg")
    mrgtbl$CumMarg = cumsum(mrgtbl$Marg)
    mrgtbl$CumMin = mrgtbl$CumMarg - mrgtbl$Marg
    mrgtbl$CumAvg = (mrgtbl$CumMarg + mrgtbl$CumMin) / 2
    return(mrgtbl)
}

prbtlike = function(prs,dat) {
    # Normal likelihood for data "censored" at 0 and 1
    mu = prs[1]
    sig = exp(prs[2])    
    n0 = length(dat[dat == 0.0])
    n1 = length(dat[dat == 1.0])
    y2 = dat[dat > 0.0 & dat < 1.0]

    p0 = pnorm(0.005,mean=mu,sd=sig,log.p=FALSE)
    p1 = 1.0 - pnorm(0.995,mean=mu,sd=sig,log.p=FALSE)
    p2 = pnorm(y2 + 0.005,mean=mu,sd=sig,log.p=FALSE) - 
         pnorm(y2 - 0.005,mean=mu,sd=sig,log.p=FALSE)
    
    llk = n0 * log(p0) + n1 * log(p1) + sum(log(p2))
    return(-1.0*llk)
}

prbmle = function(dfrm,yvar,brks=c(0,1)) { 
    # Find the probit model MLE and do some processing
    # yvar is the name of the response variable
    # brks is a vector of break points for evaluating the cdf
    o1 = nlm(prbtlike,c(0.2,-0.2),dat=dfrm[,yvar])
    mu = o1$estimate[1]
    sig = exp(o1$estimate[2])
    pvc = pnorm(brks,mean=mu,sd=sig)
    yctout = seq(1,length(brks)+1)
    ymin = c(0,pvc)
    ymax = c(pvc,1)
    dtout = data.frame(YCat=yctout,ymin=ymin,ymax=ymax,
                       mu=rep(mu,length(ymin)),sig=rep(sig,length(ymin)))
    return(dtout)
}

