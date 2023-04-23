library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT g.neighbourhood_cleansed, r.review_scores_rating FROM geolocation_edinburgh g, reviews_edinburgh r WHERE g.id_listing = r.id_listing")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

ggplot(df, aes(x = reorder(neighbourhood_cleansed, -review_scores_rating), y = review_scores_rating)) +
  stat_summary(fun = mean, geom = "bar", fill = "blue", color = "black", width = 0.7) +
  labs(x = "Barri", y = "Valoració global", title = "Valoració global mitjana en funció del barri") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1), plot.title = element_text(hjust = 0.5))

ggsave("review_scores_by_neighbourhood_edinburgh.png", width = 12, height = 7, dpi = 300)
