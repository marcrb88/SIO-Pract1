library(RMySQL)
library(ggplot2)
library(dplyr)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT host_id, host_response_time FROM hosts WHERE host_id IN (SELECT host_id FROM edinburgh)")
data <- dbFetch(result, n=-1)
final_df <- data.frame(data)

df <- data.frame(host_id = numeric(), reviews_mean = numeric())

for (h_id in final_df$host_id) {
    query1 <- paste("SELECT AVG(r.review_scores_rating) FROM edinburgh e, reviews_edinburgh r WHERE e.host_id = ", h_id)
    query2 <- paste(query1, " AND e.id = r.id_listing")
    result <- dbSendQuery(conn, query2)
    data <- dbFetch(result, n=-1)
    temp_df <- data.frame(data)
    new_row <- data.frame(host_id = h_id, reviews_mean = temp_df[1, 1])
    df <- rbind(df, new_row)
}

final_df <- merge(final_df, df, by = "host_id", all.x = TRUE)

ggplot(final_df, aes(x=host_response_time, y=reviews_mean)) +
    stat_summary(fun=mean, geom="bar", fill="steelblue") +
    labs(x = "Host Response Time", y = "Reviews Score Mean") +
    ylim(0, 5)

ggsave("review_scores_mean_by_host_response_time_edinburgh.png", width = 7, height = 5, dpi = 300)
