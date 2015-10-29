list.of.packages <- c("SciencesPo", "scales", "ggplot2","plyr", "coda","rjags","dplyr", "Rcpp", "reshape2", "repmis", "DirichletReg", "stringr", "mgcv", "nlme", "splines", "MASS", "forecast","digest", "XML", "testthat", "coefplot","mnormt","directlabels", "RJSONIO", "xtable","arm")

new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)
