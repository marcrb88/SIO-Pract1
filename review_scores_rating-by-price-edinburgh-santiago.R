library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

result <- dbSendQuery(conn, "SELECT id_listing, review_scores_rating FROM reviews_edinburgh")
data <- dbFetch(result, n=-1)
df_edinburgh <- data.frame(data)

fillable_df <- data.frame(id_listing = numeric(), price = numeric(), city = character())

for (listing in df_edinburgh$id_listing) {
    query <- paste("SELECT price FROM edinburgh WHERE id = ", listing)
    result <- dbSendQuery(conn, query)
    data <- dbFetch(result, n=-1)
    temp_df <- data.frame(data)
    new_row <- data.frame(id_listing = listing, price = temp_df[1, 1], city = "edinburgh")
    fillable_df <- rbind(fillable_df, new_row)
}

df_edinburgh <- merge(df_edinburgh, fillable_df, by = "id_listing", all.x = TRUE)




result <- dbSendQuery(conn, "SELECT id_listing, review_scores_rating FROM reviews_santiago")
data <- dbFetch(result, n=-1)
df_santiago <- data.frame(data)

fillable_df <- data.frame(id_listing = numeric(), price = numeric(), city = character())

for (listing in df_santiago$id_listing) {
    query <- paste("SELECT price FROM santiago WHERE id = ", listing)
    result <- dbSendQuery(conn, query)
    data <- dbFetch(result, n=-1)
    temp_df <- data.frame(data)
    new_row <- data.frame(id_listing = listing, price = temp_df[1, 1], city = "santiago")
    fillable_df <- rbind(fillable_df, new_row)
}

df_santiago <- merge(df_santiago, fillable_df, by = "id_listing", all.x = TRUE)




df <- rbind(df_edinburgh, df_santiago)

reg_edinburgh <- lm(price~review_scores_rating, data=df, subset=city=="edinburgh")
reg_santiago <- lm(price~review_scores_rating, data=df, subset=city=="santiago")

df$city <- factor(df$city)

plot(x=df$review_scores_rating, y=df$price,
    col = rainbow(2)[c(df$city)], pch=16,
    main = "Correlació entre les valoracions globals i el preu",
    xlab = "Valoracions globals", ylab = "Preu",
)
abline(reg_edinburgh, col="red")
abline(reg_santiago, col="blue")
legend("top", pch=16, col=rainbow(2), legend=c("Edinburgh", "Santiago"))
