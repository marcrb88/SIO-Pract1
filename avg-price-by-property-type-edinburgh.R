library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT price, property_type FROM edinburgh")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

ggplot(df, aes(x = property_type, y = price)) +
  stat_summary(fun = mean, geom = "bar", fill = "blue") +
  labs(x = "Property Type", y = "Price", title = "Average Price by Property Type") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

ggsave("avg_price_by_property_type_edinburgh.png", width = 7, height = 4, dpi = 300)
