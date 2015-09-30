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

run_sim <- function(n, days) {
  Message <- data.frame(
    Message = seq(1,n)
  )
  Message$last_sent <- as.Date(NA)
  
  next_message <- function(i) {
    today <- Sys.Date() + i
    if(sum(!is.na(Message$last_sent)) == 0) {
      min_date <- today
    } else {
      min_date <- min(Message$last_sent, na.rm=TRUE)  
    }
    
    ages <- ifelse(is.na(Message$last_sent), today - min_date, today - Message$last_sent) + 1
    
    msg <- sample(Message$Message, 1, prob = round(1.25^ages))
    
    Message[msg, "last_sent"] <<- today
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
  return(list("ans"=ans,"results"=results))
}
out <-run_sim(100, 365)
ans <- out$ans
results <- out$results
plot(results$dist)
