* 
pwcorr vshare tshare, sig

* Do some linear regression inspection 
gen tshare2 = tshare^2

regress vshare tshare tshare2

* Save the fitted values and residuals and draw the diagnostic plots.
predict yhat, xb

* predictions for just the sample on which we fit the model
predict yhat if e(sample), xb

* Compute the standard error 
predict sdres if e(sample), rstandard

* Compute the residual
predict res if e(sample), residuals

 * Square the residual, and rescale it so that the squared values
* have a mean of 1. This is needed for the eventual test statistic.
gen esq = res^2 / (res(rss)/res(N))


*The Breusch-Pagan test is a test for linear forms of heteroskedasticity
estat hettest

*Obtain White's test for heteroskedasticity, which is actually a special case of Breusch-Pagan
imtest, white
*or then manually: squared error as a function of tshare. 
gen sqsdres = sdres*sdres
lowess sqsdres tshare
// The plot produced indicates that squared error is a positive function of
// time advertising, until ~ 300 seconds, then it becomes a negative function. 
// The remedy for heteroskedasticity is simple. White developed 
// an estimator for standard errors that is robust to the presence of 
// heteroskedasticity. Note that this solution applies only to large samples. 
// For small samples, bootstrapped standard errors are preferable.
// White's test is an asymptotic test (a test focused on large samples),
// and the current sample is very small, so the results obtained from this test 
// must be interpreted with caution.

 
predict c, cooksd


* plots
* residuous are ok
hist sdres, frequency normal

hist yhat, frequency normal

twoway (scatter res yhat) (lfit res yhat) (lfitci res yhat)


* Do some bootstrapping 
bootstrap _b[_cons] _b[tshare] _b[tshare2], nodots reps(1000) saving(bsreg): regress vshare tshare tshare2  
estat bootstrap, all
*If the user is uncertain about the assumptions underlying the regression model
regress vshare tshare tshare2, vce(bootstrap, reps(500) bca seed(1))
estat bootstrap, all
*The following bootstraps the predicted value on the dogs scale for somebody who scores a 25 on the cats scale:
bootstrap pred=(_b[_cons] + _b[tshare]*300 + _b[tshare2]*300), reps(500) seed(1): regress vshare tshare tshare2  
* time 
** Marina evolution 2010 --> 2014
di 123/83
di 19.33*1.4819277
//with such an increase in ads slot, PSB is expected to fare better.
  
 ** PSDB evolution 2010 --> 2014
di (4*60)+35
di 275/438
//with such a decreasing, PSDB is expected to fare worse.
di 32*.62785388 


 ** PT evolution 2010 --> 2014
di (11*60)+24
di 684/639
//with such an increase, PT is expected to fare better.
di 1.0704225*46.91
