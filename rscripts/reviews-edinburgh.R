library(RMySQL)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location FROM reviews_edinburgh")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

print(cor(df))
