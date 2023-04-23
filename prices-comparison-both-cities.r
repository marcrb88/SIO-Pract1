source("conversion-rates.R")

library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user = "root", password = "", dbname = "pract1", host = "localhost")

# Get prizes from edinburgh
result <- dbSendQuery(conn, "SELECT price FROM edinburgh")
edinburgh_prices <- dbFetch(result, n = -1)
df_edinburgh <- data.frame(edinburgh_prices)

# Get prizes from santiago
result2 <- dbSendQuery(conn, "SELECT price FROM santiago")
santiago_prices <- dbFetch(result2, n = -1)
df_santiago <- data.frame(santiago_prices)

df_edinburgh$price <- df_edinburgh$price * GBP_TO_USD_RATE
df_santiago$price <- df_santiago$price * CLP_TO_USD_RATE

df_edinburgh <- subset(df_edinburgh, price <= 2000)
df_santiago <- subset(df_santiago, price <= 2000)



hist(df_edinburgh$price,
    breaks = 16,
    main = "Preu d'allotjaments i freqüències absolutes",
    xlab = "Preu (USD)",
    ylab = "Freqüències",
    xlim = c(0, 1000),
    ylim = c(0, 7000),
    col = "#ff0000"
)

hist(df_santiago$price,
    breaks = 16,
    xlim = c(0, 1000),
    ylim = c(0, 7000),
    add = TRUE,
    col = "#0000ff3b",
)

legend("topright",
    legend = c("Edinburgh", "Santiago"),
    col = c("#ff0000", "#0000ff3b"),
    pt.cex = 2, pch = 15
)