library(data.table)
library(rJava)
library(xlsx)
library(stringr)
source('analysis/exploratory_helper.R')
data.sentences <- unique(fread('~/do/data/result/result_09May2016-02-40-17-full-pool-preb-food-diet.csv', 
                        sep='\t', colClasses = "character", select=1:8))

GetWriteRankedCatalog <- function(data.sentences, entity.name, catalog.tidy.path){
  data.entity <- GetEntityData(data.sentences, entity.name)
  data.entity.count <- data.entity[,.N,by=entity.name]
  
  catalog.entity <- data.table(readLines(catalog.tidy.path))
  setnames(catalog.entity, c(entity.name))
  catalog.entity.ranked <- unique(merge(catalog.entity, data.entity.count, by=entity.name, all.x=T, all.y=T))
  catalog.entity.ranked[is.na(N),N:=0]
  setorder(catalog.entity.ranked, -N)
  
  write.xlsx(catalog.entity.ranked, file=paste0(entity.name, "-ranked.xlsx"))
  catalog.entity.ranked
}

######
# legacy code
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
###########

GetWriteRankedCatalog(data.sentences, "diet", "data/diet/diets_tidy.csv")
GetWriteRankedCatalog(data.sentences, "prebiotic", "data/prebiotic/prebiotics_tidy.csv")
GetWriteRankedCatalog(data.sentences, "food", "data/food/food_mixed_tidy.csv")

data.bacteria <- GetEntityData(data.sentences, "bacteria")
data.bacteria.count <- data.bacteria[,.N,by=bacteria_id]
data.bacteria.unique <- data.bacteria[,.(bacteria, bacteria_id)]
setkey(data.bacteria.unique, bacteria_id)
data.bacteria.unique <- unique(data.bacteria.unique)
data.bacteria.count <- merge(data.bacteria.count, data.bacteria.unique, by='bacteria_id')
setorder(data.bacteria.count, -N)
write.xlsx(data.bacteria.count, file=paste0("bacteria-ranked.xlsx"))

data.sentences$prebiotic <- str_replace_all(data.sentences$prebiotic, ";noid", "")
data.sentences$diet <- str_replace_all(data.sentences$diet, ";noid", "")
data.sentences$food <- str_replace_all(data.sentences$food, ";nogroup", "")
write.xlsx(data.sentences, file=paste0("sentences-bact-prebiotic-food-diet.xlsx"))
