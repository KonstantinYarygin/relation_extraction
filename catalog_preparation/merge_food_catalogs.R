data.usda <- fread('data/food/food_usda_tidy.csv')
data.dbpedia <- data.table(readLines('data/food/food_dbpedia_tidy.csv'))
setnames(data.dbpedia, c("name"))
data.exclude <- data.table(readLines('data/food/food_exclude.csv'))
setnames(data.exclude, c("name"))

data.mixed <- c(data.usda$name, data.dbpedia$name)
data.mixed.sub <- data.mixed[which(!(data.mixed %in% data.exclude$name))]

write(data.mixed.sub, "data/food/food_mixed_tidy.csv")
