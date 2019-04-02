Argentine Forecasting 
========================================================

This is a document explaining how to run the bayesian dynamic linear model used to forecast the Argentine's presidential election and published periodically at  [daniemarcelino.com](http://www.danielmarcelino.com). The Program used to generate predictions is based on [R](http://www.r-project.org/) code and is contained in a repository on github.

Below is an example of loading required packages to generate the predictions.

## Preparations
### Installing the R-package

As the first step we need to install the package from github to [R](http://www.r-project.org/). Just fire up [R](http://www.r-project.org/) and run the following code.

### Downloading polling data 

We use the polling data from Argentine that is contained in the Argentine github repo. We download the data as ```polls``` the following way:


```r
url <- "https://github.com/danielmarcelino/Argentine/raw/master/Data/polls.csv"

polls <- repmis::source_data(data_url, sep = ",", dec = ".", header = TRUE)
```
