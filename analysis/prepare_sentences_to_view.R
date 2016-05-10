library(data.table)
library(xlsx)
library(stringr)
source("analysis/exploratory_helper.R")
data <- unique(fread('~/do/data/result/result_09May2016-02-40-17-full-pool-preb-food-diet.csv', 
                     sep='\t', colClasses = "character", select=1:8))
###
data$text <- str_replace_all(data$text, ";", ",")
data$article_title <- str_replace_all(data$article_title, ";", ",")
data$journal <- str_replace_all(data$journal, ";", ",")
data$prebiotic <-  str_replace_all(data$prebiotic, ";noid", "")
data$diet <-  str_replace_all(data$diet, ";noid", "")
data$food <-  str_replace_all(data$food, ";nogroup", "")
###
data.to.find <- fread('~/Downloads/Dietary associations - unparsed.tsv', sep='\t')
data.to.find.sub <- data.to.find[,.(V1, V2, V3, V4)]
data.to.find.sub$order <- 1:nrow(data.to.find.sub)
setnames(data.to.find.sub, c("number", "text", "article_title", "journal", "order"))
data.merged <- merge(data.to.find.sub, data, by=c("text", "article_title", "journal"), all.x = T)
setcolorder(data.merged, c("order", "number", "text", "article_title", "journal", "pmc", "bacteria", "prebiotic", "diet", "food"))
setorder(data.merged, order)
write.xlsx(data.merged, "merged.xlsx")
###

data.bacteria <- GetBacteria(data)
setkey(data.bacteria, text,article_title,journal)
setkey(data, text,article_title,journal)
data.merged <- merge(data.bacteria, data, by=c("text","article_title","journal"))
setcolorder(data.merged, c("text","article_title","journal", "pmc", 
                           "bacteria.x", "bacteria_code", "bacteria.y", "prebiotic", "diet", "food"))

setnames(data.merged, c("text","article_title","journal", "pmc", 
                           "bacteria", "bacteria_code", "all_bacteria", "prebiotic", "diet", "food"))

data.merged$text <- str_replace_all(data.merged$text, ";", ",")
data.merged$article_title <- str_replace_all(data.merged$article_title, ";", ",")
data.merged$journal <- str_replace_all(data.merged$journal, ";", ",")
data.merged$all_bacteria <-  str_replace_all(data.merged$all_bacteria, ";", "-")
data.merged$prebiotic <-  str_replace_all(data.merged$prebiotic, ";noid", "")
data.merged$diet <-  str_replace_all(data.merged$diet, ";noid", "")
data.merged$food <-  str_replace_all(data.merged$food, ";nogroup", "")

data.merged[,{
  file <- paste0(.SD$bacteria[1], '-', bacteria_code, '.csv')
  file <- str_replace_all(file, "/", "_")
  # message(file)
  path <- file.path('analysis', 'result_view', file)
  message(path)
  write.table(.SD, file = path, row.names = F, col.names = T, quote = F, sep = '\t')
}, by=bacteria_code]
