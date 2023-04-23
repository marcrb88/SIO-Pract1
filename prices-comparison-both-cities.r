library(RMySQL)
library(ggplot2)

lapply(dbListConnections(dbDriver(drv = "MySQL")), dbDisconnect)
conn <- dbConnect(MySQL(), user="root", password="", dbname="pract1", host="localhost")

# Get prizes from edinburgh
result <- dbSendQuery(conn, "SELECT price FROM edinburgh")
edinburgh_prizes <- dbFetch(result, n=-1)
df_edinburgh <- data.frame(edinburgh_prizes)

# Get prizes from santiago
result2 <- dbSendQuery(conn, "SELECT price FROM santiago")
santiago_prizes <- dbFetch(result2, n=-1)
df_santiago <- data.frame(santiago_prizes)

# Get subset of the data from edinburgh
df_subset_edinburgh <- data.frame(z = df_edinburgh[df_edinburgh$price < 1000, "price"])
names(df_subset_edinburgh)[1] <- "price"

# Get subset of the data from santiago
df_subset_santiago <- data.frame(z = df_santiago[df_santiago$price < 1000, "price"])
names(df_subset_santiago)[1] <- "price"


hist(df_subset_santiago$price,
breaks=16,
main="Distribución del salario",
xlab="Precio",
ylab="Frecuencia",
xlim=c(0,1000),
ylim=c(0,6000),
col="#ff0000"
)
hist(df_subset_edinburgh$price,
breaks=16,
xlim=c(0,1000),
ylim=c(0,6000),
add = TRUE,
col="#0000ff3b",
)
legend("topright", legend = c("santiago", "edinburgh"),
col=c("#ff0000", "#0000ff3b"),
pt.cex = 2, pch = 15
)