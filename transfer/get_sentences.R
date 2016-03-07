library(data.table)
library(ggplot2)
library(stringr)
library(plyr)

OUT_FILE_NAME <- "sentences_replaced.txt"

data <- fread('~/Downloads/sentences17_50_46-01_03_16.csv', sep=',')

# parse bacteria, nutrients, diseases
data.bacteria = data[,
                     .(unlist(llply(str_match_all(bacteria, '\'([^\\)]+)\''), .fun=function(x) x[,2])),
                       unlist(llply(str_match_all(bacteria, '(\\d+)\\)'), .fun=function(x) x[,2]))),
                     by=.(text, article_title)]
setnames(data.bacteria, c("text","article_title","bacteria","bacteria_code"))

data.nutrient = data[,
                     .(unlist(llply(str_match_all(nutrients, '\'([^\\)]+)\','), .fun=function(x) x[,2])),
                     unlist(llply(str_match_all(nutrients, ',\\s\'([^\\)]+)\''), .fun=function(x) x[,2]))),
                     by=.(text, article_title)]
setnames(data.nutrient, c("text","article_title","nutrient","nutrient_code"))

data.disease = data[,.(unlist(llply(str_match_all(diseases, 
                                                  '\'([^\\)]+)\','), 
                                    .fun=function(x) x[,2])),
                       unlist(llply(str_match_all(diseases, 
                                                  ',\\s\'([^\\)]+)\''), 
                                    .fun=function(x) x[,2]))),
                    by=.(text, article_title)]

setnames(data.disease, c("text","article_title","disease","disease_code"))

# get unique because anyway we'll replace all words in a sentence with a single command
data.bacteria <- unique(data.bacteria)
data.nutrient <- unique(data.nutrient)
data.disease <- unique(data.disease)

# making universal names
data.bacteria[,universal:=paste("BACTERIA", .GRP, sep=""), by=bacteria_code]
data.nutrient[,universal:=paste("NUTRIENT", .GRP, sep=""), by=nutrient_code]
data.disease[,universal:=paste("DISEASE", .GRP, sep=""), by=disease_code]


bacterias <- unique(data.bacteria[,.(bacteria, universal)])
nutrients <- unique(data.nutrient[,.(nutrient, universal)])
diseases <- unique(data.disease[,.(disease, universal)])
sentences <- unique(data$text)

data.merged <- merge(data.bacteria, data.nutrient, by = c("text","article_title"), all = TRUE)
data.merged <- merge(data.merged, data.disease, by = c("text","article_title"), all = TRUE)

data.merged$text_replaced <- str_replace_all(data.merged$text, 
                     data.merged$bacteria, 
                     rep("BACTERIA", nrow(data.merged)))
data.merged$text_replaced <- str_replace_all(data.merged$text_replaced, 
                                            data.merged$nutrient, 
                                            rep("BACTERIA", nrow(data.merged)))

for (i in 1:nrow(bacterias)){
  bacteria <- bacterias$bacteria[i]
  universal <- bacterias$universal[i]
  sentences <- str_replace(string = sentences, 
                           pattern = bacteria, 
                           replacement = universal)
  message(paste("bacteria",i, sep = " "))
}
for (i in 1:nrow(nutrients)){
  nutrient <- nutrients$nutrient[i]
  universal <- nutrients$universal[i]
  sentences <- str_replace(string = sentences, 
                           pattern = nutrient, 
                           replacement = universal)
  message(paste("nutrient",i, sep = " "))
}
for (i in 1:nrow(diseases)){
  disease <- diseases$disease[i]
  universal <- diseases$universal[i]
  sentences <- str_replace(string = sentences, 
                           pattern = disease, 
                           replacement = universal)
  message(paste("disease",i, sep = " "))
}

data.sentences <- data.table(sentences)
write(sentences, OUT_FILE_NAME)
