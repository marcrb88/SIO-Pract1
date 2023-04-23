source("conversion-rates.R")

library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT id, price from edinburgh")
data <- dbFetch(result, n=-1)
df <- data.frame(data)

fillable_df <- data.frame(id = numeric(), number_of_amenities = numeric())

for (listing_id in df$id) {
    query <- paste("SELECT COUNT(*) FROM listing_amenities_edinburgh WHERE id_listing = ", listing_id)
    result <- dbSendQuery(conn, query)
    data <- dbFetch(result, n=-1)
    temp_df <- data.frame(data)
    new_row <- data.frame(id = listing_id, number_of_amenities = temp_df[1, 1])
    fillable_df <- rbind(fillable_df, new_row)
}

df <- merge(df, fillable_df, by = "id", all.x = TRUE)

df$price <- df$price * GBP_TO_USD_RATE

df <- subset(df, price <= 2000)

plot(x=df$number_of_amenities, y=df$price,
    main = "Correlació entre el número de comoditats i el preu",
    xlab = "Número de comoditats", ylab = "Preu (USD)",
    col=rgb(0.8, 0.2, 0.2), pch=20)
abline(lm(df$price~df$number_of_amenities), lwd=3,
    col=rgb(0.2, 0.2, 0.8, 0.8))
