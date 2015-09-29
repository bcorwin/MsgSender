library(plyr)

Message <- data.frame(
  Message = seq(1,100)
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
  
  msg <- sample(Message$Message, 1, prob = ages)
  Message[msg, "last_sent"] <<- today
  return(msg)
}


results <- NULL
for(i in seq(0, 365)) {
  add <- data.frame(date=i, msg=next_message(i))
  results <- rbind(results, add)
}

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

ans <- ddply(results, "msg", summarize,
             Count = length(date),
             Avg.Dist = avg_dist(date))
