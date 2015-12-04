---
title: "Venezuelan Parliamentary Elections"
author: "Daniel Marcelino"
date: "December 03, 2015"
output: html_document
---

```{r header, results = 'hide', echo = FALSE, message = FALSE}

setwd("~/Polling/Venezuela")

knitr::opts_chunk[["set"]](cache =TRUE,
                           fig.path = "figures/venezuela-",
                           dev = 'png',
                           fig.height = 4, fig.width = 6,
                           autodep = TRUE)
library("rstan")
library("ggplot2")
library("dplyr")
library("tidyr")
require("readxl")
require("lubridate")
library("SciencesPo")
library("loo")
library("xtable")
library("reshape2")
options(mc.cores = parallel::detectCores())

this <- new.env()

tab_path <- "../analysis/tex"
dir.create(tab_path, showWarnings = FALSE)

STAN_DIR <- "./stan/"
SEED <- 2015

theme_local <- theme_538()
```



```{r helper_funs}
omega_summary <- function(x, param = "omega", k = 1) {
  melt(rstan::extract(x, param)[[1]],
       varnames = c("iter", "time", "dim")) %>%
    group_by(dim, time) %>%
    summarize(mean = mean(value),
              sd = sd(value),
              p025 = quantile(value, 0.025),
              p16 = quantile(value, 0.16),
              p25 = quantile(value, 0.25),
              median = median(value),
              p75 = quantile(value, 0.75),
              p84 = quantile(value, 0.84),
              p975 = quantile(value, 0.975))
}

omega_plot <- function(.data, k = 1) {
  dat <- bind_cols(filter(.data, dim == k),
                   select(BushApproval, end_date))
  ggplot(dat, aes(x = end_date)) +
    geom_hline(yintercept = 0, colour = "gray") +
    #geom_linerange(mapping = aes(ymin = p025, ymax = p975), colour = "gray") +
    #geom_point(mapping = aes(y = mean)) +
    geom_line(mapping = aes(y = mean)) +
    theme_538() +
    theme(panel.grid = element_blank())
}

mu_summary <- function(x, param = "mu") {
  melt(rstan::extract(x, param)[[1]],
       varnames = c("iter", "time", "dim")) %>%
    group_by(dim, time) %>%
    summarize(mean = mean(value),
              sd = sd(value),
              p025 = quantile(value, 0.025),
              p16 = quantile(value, 0.16),
              p25 = quantile(value, 0.25),
              median = median(value),
              p75 = quantile(value, 0.75),
              p84 = quantile(value, 0.84),
              p975 = quantile(value, 0.975))
}

mu_plot <- function(.data) {
  dat <- filter(.data, dim == 1, time > 1) %>%
    bind_cols(BushApproval)
  ggplot(dat, aes(x = end_date)) +
    geom_ribbon(mapping = aes(ymin = p16, ymax = p84),
                alpha = 0.3) +
    geom_ribbon(mapping = aes(ymin = p025, ymax = p975),
                alpha = 0.3) +
    geom_point(mapping = aes(y = approve), size = 1) +
    geom_line(mapping = aes(y = mean)) +
    ylab("% Approve") +
    xlab("") +
    theme_538()
}

dlm_err <- function(x, param = "dlm") {
  rstan::extract(x, param)[[1]][ , -1, 13]
}

```

```{r data}
data <- read_excel("polls.xlsx")
data$begin <- as.Date(data$begin, format = "%d-%m-%Y")
#data$election <- as.numeric(as.character(as.Date("06-12-2015", format = "%d-%m-%Y") - data$begin))
data <- data %>% filter(begin>as.Date("01-07-2014", format = "%d-%m-%Y")

long <- data %>% gather(party, value, -c(house, begin)) %>% filter(party=="MUD" | party=="PSUV" | party=="Others" | party=="Undecided") %>% arrange(begin)
```

```{r simpleplot, fig.height = 3, fig.width = 6}
ggplot(data) +
  geom_point(aes(x = begin, y = MUD,size=3),color="gray30") +
  geom_point(aes(x = begin, y = PSUV,size=3), color="tomato") +
  theme_538() +
  xlab("") +
  ylab("% Vote intentions") +
  plotTitleSubtitle("Vote Intentions for the Gop (MUD) and Gov't (PSUV)", "Black = MUD, Red = PSUV")
  theme_bw() +
    # Set the entire chart region to a light gray color
    theme(panel.background=element_rect(fill="#F0F0F0")) +
    theme(plot.background=element_rect(fill="#F0F0F0")) +
    theme(panel.border=element_rect(colour="#F0F0F0")) +
    # Format the grid
    theme(panel.grid.major=element_line(colour="#D0D0D0",size=.75)) +
    scale_x_continuous(minor_breaks=0,breaks=seq(0,1,.10),limits=c(0,1)) +
    scale_y_continuous(minor_breaks=0,breaks=seq(0,.6,.2),limits=c(0,.25)) +
    theme(axis.ticks=element_blank()) +
    # Dispose of the legend
    theme(legend.position="none") +
    # Set title and axis labels, and format these and tick marks
    ggtitle("Some Random Data I Made") +
    theme(plot.title=element_text(face="bold",hjust=-.08,vjust=2,colour="#3C3C3C",size=20)) +
    ylab("Data Label") +
    xlab("Days Since Beginning") +
    theme(axis.text.x=element_text(size=11,colour="#535353",face="bold")) +
    theme(axis.text.y=element_text(size=11,colour="#535353",face="bold")) +
    theme(axis.title.y=element_text(size=11,colour="#535353",face="bold",vjust=1.5)) +
    theme(axis.title.x=element_text(size=11,colour="#535353",face="bold",vjust=-.5)) +
    # Big bold line at y=0
    geom_hline(yintercept=0,size=1.2,colour="#535353") +
    # Plot margins and finally line annotations
    theme(plot.margin = unit(c(1, 1, .5, .7), "cm"))

```

## Normal

```{r m1}
m1 <- stan_model(file.path(STAN_DIR, "poly_normal.stan"))
```

```{r m1_ret}
m1_data <-
  within(list(), {
    y <- matrix(BushApproval$approve)
    n <- length(y)
    p <- 2
    miss <- matrix(as.integer(is.na(y)))
    m0 <- c(BushApproval$approve[1], 0)
    C0 <- matrix(c(2, 1, 1, 1), 2, 2) * rep(var(BushApproval$approve[1:10]) * 2, 2)
    s <- sqrt(0.5 * (1 - 0.5) / 500) # standard error of poll of size 500
    w <- rep(1, 2)
  })

m1_ret <- sampling(m1, data = m1_data, seed = SEED)
```

```{r m1_mu}
m1_mu <- mu_summary(m1_ret)
mu_plot(m1_mu)

```

```{r m1_omega}
m1_omega <- rstan::extract(m1_ret, "omega")[[1]]
plot(apply(m1_omega, 2:3, mean)[ , 1], type = "l")
plot(apply(m1_omega, 2:3, mean)[ , 2], type = "l")
```

## Horseshoe

```{r m2}
m2 <- stan_model(file.path(STAN_DIR, "poly_horseshoe.stan"))
```


```{r m2_ret}
m2_data <-
  within(m1_data, {
    w <- rep(1 / n, 2)
  })
m2_ret <- sampling(m2, data = m2_data, seed = SEED)
```

```{r m2_ret_summary}
summary(m2_ret, par = c("sigma", "tau"))
```

```{r m2_mu}
m2_mu <- mu_summary(m2_ret)
mu_plot(m2_mu)
```

```{r m2_omega_1}
m2_omega <- omega_summary(m2_ret)
omega_plot(m2_omega, k = 1)
```

```{r m2_omega_2}
omega_plot(m2_omega, k = 2)
```



## Normal with interventions

```{r m3}
m3 <- stan_model(file.path(STAN_DIR, "poly_normal_intervention.stan"))
```

```{r m3_ret}
m3_data <-
  within(m1_data, {
    intervention <- c(23, 86)
    n_intervention <- length(intervention)
  })
m3_ret <- sampling(m3, data = m3_data, seed = SEED)
```

```{r m3_mu}
m3_mu <- mu_summary(m3_ret)
mu_plot(m3_mu)
```

```{r m3_omega_1}
m3_omega <- omega_summary(m3_ret)
omega_plot(m3_omega, k = 1)
```

```{r m3_omega_2}
omega_plot(m3_omega, k = 2)
```



## Horseshoe+

```{r m4}
m4 <- stan_model(file.path(STAN_DIR, "poly_horseshoeplus.stan"))
```


```{r mu4_ret}
m4_data <-
  within(m1_data, {
    w <- c(1/n, 1/ n)
  })
m4_ret <- sampling(m4, data = m4_data, seed = SEED)
```

```{r m4_ret_summary}
summary(m4_ret, par = c("sigma", "tau"))
```

```{r m4_mu}
m4_mu <- mu_summary(m4_ret)
mu_plot(m4_mu)
```

```{r m4_omega_1}
m4_omega <- omega_summary(m4_ret)
omega_plot(m4_omega, k = 1)
```

```{r m4_omega_2}
omega_plot(m4_omega, k = 2)
```



## Model Comparison

```{r model_comp}
waic2df <- function(x) {
  x_waic <- waic(x)
  x_loo <- loo(x)
  bind_cols(as_data_frame(x_waic[! names(x_waic) %in% c("pointwise")]),
            as_data_frame(x_loo[! names(x_loo) %in% c("pointwise", "pareto_k")]))
}

msae <- function(err) {
  mse <- sqrt(mean((apply(err, 2, mean))^2))
  mae <- mean(abs(apply(err, 2, mean)))
  data_frame(mse = mse, mae = mae)
}

waic_loo <-
  list(mutate(waic2df(drop(rstan::extract(m1_ret, "log_lik")[[1]])),
              model = "\\ModelII{Normal}"),
       mutate(waic2df(drop(rstan::extract(m3_ret, "log_lik")[[1]])),
              model = "\\ModelII{Intervention}"),
       mutate(waic2df(drop(rstan::extract(m2_ret, "log_lik")[[1]])),
              model = "\\ModelII{Horseshoe}"),
       mutate(waic2df(drop(rstan::extract(m4_ret, "log_lik")[[1]])),
              model = "\\ModelII{Horseshoe+}")) %>%
  bind_rows()

mse_mae <-
  list(mutate(msae(dlm_err(m1_ret)),
              model = "\\ModelII{Normal}"),
       mutate(msae(dlm_err(m3_ret)),
              model = "\\ModelII{Intervention}"),
       mutate(msae(dlm_err(m2_ret)),
              model = "\\ModelII{Horseshoe}"),
       mutate(msae(dlm_err(m4_ret)),
              model = "\\ModelII{Horseshoe+}")) %>%
  bind_rows()

model_comp <- left_join(waic_loo, mse_mae, by = "model")

model_comp %>%
  select(model, mse, elpd_waic, elpd_loo) %>%
  rename(`$\\mathrm{RMSE}$` = mse,
         `$\\mathrm{elpd}_{WAIC}$` = elpd_waic,
         `$\\mathrm{elpd}_{loo}$` = elpd_loo)  %>%
  xtable() %>%
  print(sanitize.text = identity,
        floating = FALSE,
        include.rownames = FALSE,
        type = "latex",
        file = file.path(tab_path, "bush-tab_model_comp.tex"))
```



## Save Data

```{r save}
saveRDS(as.list(this), file = "bush.rds")
```


