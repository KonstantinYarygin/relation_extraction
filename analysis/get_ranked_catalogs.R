library(data.table)
library(rJava)
library(xlsx)
source('exploratory_helper.R')
data.sentences <- fread('~/do/data/result/result_05May2016-07-50-01-digital-ocean.csv')

parsed <- GetBacteriaNutrientDiseaseFood(data.sentences)
data.disease <- parsed$disease
data.food <- parsed$food

# paths specified from analysis directory
catalog.disease <- fread('../data/diseases/diseases.csv')
catalog.food <- fread('../data/food/food_dbpedia_tidy.csv', sep = '\t', header=F)
setnames(catalog.food, c("word"))

data.disease.count <- data.disease[,.N, by=disease]
data.food.count <- data.food[,.N, by=food]

catalog.disease.count <- merge(catalog.disease, data.disease.count, by.x="name", by.y="disease", all.x = T)
catalog.disease.count[is.na(N),N:=0]
catalog.disease.count[is.na(group),group:='']
catalog.disease.collapsed <- catalog.disease.count[,.(sum(N), paste(name, collapse = ", "), paste(unique(group), collapse = ", "), unique(obsolete)),by=id]
setnames(catalog.disease.collapsed, c("id", "count", "names", "groups", "obsolete"))
setorder(catalog.disease.collapsed, -count)

catalog.food.count <- merge(catalog.food, data.food.count, by.x="word", by.y="food", all.x = T)
catalog.food.count[is.na(N),N:=0]
setnames(catalog.food.count, "N", "count")
setorder(catalog.food.count, -count)

write.xlsx(catalog.disease.collapsed, file="diseases-ranked.xlsx")
write.xlsx(catalog.food.count, file="food-ranked.xlsx")
