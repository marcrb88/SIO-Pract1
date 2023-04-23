source("conversion-rates.R")

library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT price, property_type FROM santiago")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

ggplot(df, aes(x = reorder(property_type, -price), y = price * CLP_TO_USD_RATE)) +
  stat_summary(fun = mean, geom = "bar", fill = "blue") +
  labs(x = "Tipus de propietat", y = "Preu (USD)", title = "Preu mitjà en funció del tipus de propietat") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1), plot.title = element_text(hjust = 0.5)) +
  ylim(0, 2000)

ggsave("avg_price_by_property_type_santiago.png", width = 11, height = 4, dpi = 300)
