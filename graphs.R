library(RMySQL)
lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")
result <- dbSendQuery(conn, "SELECT price FROM edinburgh")
data <- dbFetch(result, n=-1)
prices <- as.numeric(data$price)
freq_table <- table(prices)
freq_table_pct <- prop.table(freq_table) * 100  # calculate relative frequency and convert to percentage
barplot(freq_table_pct, main="Frequency Distribution of Prices in Edinburgh", xlab="Price", ylab="Percentage", ylim=c(0,2.5))
