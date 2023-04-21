library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT g.neighbourhood_cleansed, r.review_scores_rating FROM geolocation_santiago g, reviews_santiago r WHERE g.id_listing = r.id_listing")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

ggplot(df, aes(x = neighbourhood_cleansed, y = review_scores_rating)) +
  geom_point() +
  labs(x = "Neighborhood", y = "Review Score", title = "Review Scores by Neighborhood") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

ggsave("review_scores_by_neighbourhood_santiago.png", width = 5, height = 7, dpi = 300)
