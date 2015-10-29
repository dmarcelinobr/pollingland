#Essentials

partyVar <- function(data, candidate) {
  ## Description:
  ## Calculate the variance of a poll when there are four candidates
  ## Args:
  ##   data - the data frame with the polls
  ##   candidate - the name of the candidate to calculate the variance
  ## Returns:
  ##  a scalar with the variance

  alpha <- data.frame(data$psdb,
                      data$pt,
                      data$prb,
                      data$others2)
  alpha <- sapply(alpha, function(x) x * data$size+0.005)

  index <- getIndex(candidate)
  var <- apply(alpha, 1, function(x) var(rdirichlet(10000, x)[,index]))
  return(var)
}
