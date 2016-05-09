library(data.table)
library(xlsx)
library(stringr)
source("analysis/exploratory_helper.R")
data <- unique(fread('~/do/data/result/result_09May2016-02-40-17-full-pool-preb-food-diet.csv', 
                     sep='\t', colClasses = "character", select=1:8))

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
