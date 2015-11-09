library(ggplot2)
library(plyr)

avg_dist <- function(dates) {
  len <- length(dates)
  if(len <= 1) {
    return(NA)
  }
  dist <- NULL
  for(i in seq(2, len)) {
    dist <- c(dist, dates[i] - dates[i-1])
  }
  return(mean(dist))
}

min_dist <- function(dates) {
  len <- length(dates)
  if(len <= 1) {
    return(NA)
  }
  dist <- NULL
  for(i in seq(2, len)) {
    dist <- c(dist, dates[i] - dates[i-1])
  }
  return(min(dist))
}

run_sim <- function(n, days,
                    func = parse(text="ages"),
                    rate_fill=parse(text="3")) {
  ratings <- NA
  start <- Sys.time()
  Message <- data.frame(
    Message = seq(1,n),
    Rating = rep(NA, n)
  )
  Message$last_sent <- as.Date(NA)
  
  next_message <- function(i) {
    today <- Sys.Date() + i
    if(sum(!is.na(Message$last_sent)) == 0) {
      min_date <- today
    } else {
      min_date <- min(Message$last_sent, na.rm=TRUE)  
    }
    
    ratings <- Message$Rating
    ratings <- ifelse(is.na(ratings), eval(rate_fill), ratings)
    
    ages <- ifelse(is.na(Message$last_sent), today - min_date, today - Message$last_sent) + 1
    
    msg <- sample(Message$Message, 1, prob = eval(func))
    
    Message[msg, "last_sent"] <<- today
    if(is.na(Message[msg, "Rating"])) {
      Message[msg, "Rating"] <<- runif(1, min = 1, max=5)
    }
    return(msg)
  }
  
  
  results <- NULL
  for(i in seq(0, days)) {
    add <- data.frame(date=i, msg=next_message(i))
    results <- rbind(results, add)
  }
  
  results$dist <- NA
  for(i in seq(2, nrow(results))) {
    cur <- results[i, ]
    prev <- results[seq(i-1), ]
    prev <- prev[prev$msg == cur$msg, ]
    prev <- prev[nrow(prev), ]
    if(length(prev$date) > 0) {
      results$dist[i] <- cur$date - prev$date
    } else {
      results$dist[i] <- NA
    }
  }
  
  ans <- ddply(results, "msg", summarize,
               Count = length(date),
               Min.Dist = min_dist(date),
               Avg.Dist = avg_dist(date))
  
  results <- merge(results, subset(Message, select = c("Message", "Rating")),
               by.x="msg", by.y="Message")
  
  results$Rating <- ifelse(is.na(results$Rating), "?",
                           as.character(round(results$Rating)))
  
  timer <- signif(Sys.time() - start, 2)
  return(list("ans"=ans,"results"=results, "func"=func, "timer"=timer, "ratings"=ratings))
}

num_simulations <- 5
out1 <-run_sim(60, 100)
out2 <-run_sim(60, 100, func = parse(text="round(1.1^ages)"))
out3 <-run_sim(60, 100, func = parse(text="10 * ages"))
out4 <-run_sim(60, 100, func = parse(text="ages^10"))
out5 <-run_sim(60, 600, func = parse(text="round((1.1*ratings)^ages)"))

ymax <- max(
  sapply(seq(1,num_simulations), function(x) {
    temp <- get(paste0("out", x))
    max(temp$results$dist, na.rm=TRUE)
  })
)
ymax <- round_any(ymax, 50, f=ceiling)

for(p in seq(1,num_simulations)) {
  temp <- get(paste0("out", p))
  title <- as.character(temp$func)
  sub <- paste0("Runtime=", temp$timer, "s")
  
  plotdata <- na.omit(temp$results)
  p <- ggplot(plotdata, aes(x=date, y=dist, color=Rating))
  p <- p + geom_point(shape=19)
  if(grepl("(?i)ratings", title)) p <- p + geom_smooth(method="loess")
  p <- p + labs(y="Day since last sent", x="Day", title = title) + ylim(0,ymax)
  plot(p)
}

# Random select number for the number of people rating.
## n = rpois(1,3)
# Randomly select the "true" rating (set this at the begining?)
## m = sample(c(1,4/3,2,4,10), 1)
# Random numbers around that average that need to be bound around
## r = round(4*rbeta(n, shape1=m, shape2=2)+1)
#Store those numbers because I'll be need to average or percentile them down the road
#Take the average (or 80th percentile, or whatever) to set as the rating
## replicate(2, mean(round(4*rbeta(rpois(1,3), shape1=sample(c(1,4/3,2,4,10), 1), shape2=2)+1)))