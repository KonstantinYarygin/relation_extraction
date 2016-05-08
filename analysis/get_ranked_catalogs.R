library(data.table)
library(rJava)
library(xlsx)
library(stringr)
source('analysis/exploratory_helper.R')
data.sentences <- fread('~/do/data/result/result_07May2016-22-08-56.csv')

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

## prebiotic
data.sentences <- data.sentences[text!="text"]

data.prebiotics <- GetPrebiotics(data.sentences)
data.prebiotics.count <- data.prebiotics[,.N,by="prebiotic"]

catalog.prebiotics <- data.table(readLines("data/prebiotic/prebiotics_tidy.csv"))
setnames(catalog.prebiotics, c("prebiotic"))
catalog.prebiotics.ranked <- unique(merge(catalog.prebiotics, data.prebiotics.count, by="prebiotic", all.x=T))
catalog.prebiotics.ranked[N==NA,N:=0]
setorder(catalog.prebiotics.ranked)

data.bacteria.prebiotic <- data.sentences[,.(text, article_title, journal, bacteria, prebiotic)]
data.bacteria.prebiotic$prebiotic <- str_replace_all(data.bacteria.prebiotic$prebiotic, ";noid", "")
write.xlsx(catalog.prebiotics.ranked, file="prebiotics-ranked.xlsx")
write.xlsx(data.bacteria.prebiotic, file="prebiotics-sentences.xlsx")
