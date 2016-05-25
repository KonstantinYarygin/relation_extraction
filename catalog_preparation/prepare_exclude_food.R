library(data.table)

food.usda.marked <- fread("data/food/food-ranked-usda-marked.csv")
food.dbpedia.marked <- fread("data/food/food-ranked-dbpedia-marked.csv")

food.usda.exclude <- food.usda.marked[exclude!=""]$word
food.dbpedia.exclude <- food.dbpedia.marked[exclude==1]$word

food.exclude <- c(food.usda.exclude, food.dbpedia.exclude)

write(food.exclude, file = "data/food/food_exclude.csv")
