library(plyr)

GetHistPlots <- function(data.count, x.variable){
  setnames(data.count, x.variable, "object")
  plot1 <- ggplot(data.count[0:10], aes(x = reorder(object, -N), y = N)) + 
    geom_bar(stat="identity") + 
    theme_bw() + 
    xlab(x.variable) + 
    ylab('count') + 
    theme(text = element_text(size=13), 
          axis.text.x = element_text(angle=10, vjust=1))
  plot2 <- ggplot(data.count, aes(x = reorder(object, -N), y = N, group=1)) + 
    geom_line(color="green", size=1) + 
    theme_bw() + 
    xlab(x.variable) + 
    ylab('count') + geom_hline(yintercept=0) +  
    theme(axis.line=element_line(colour = "grey"), axis.text.x=element_blank(), 
          axis.text.x=element_blank(), axis.ticks.x=element_blank(),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank())
  setnames(data.count, "object", x.variable)
  return(list(plot1=plot1, plot2=plot2))
}

MergePlotBactPairs <- function(data.bacteria, data.other, column.other){
  data.bacteria.other <- merge(data.bacteria, data.other, by = c("text","article_title"))
  data.bacteria.other <- unique(data.bacteria.other)
  data.bacteria.other.count <- data.bacteria.other[,.N,by=c('bacteria_code',column.other)]
  data.bacteria.other.count <- merge(data.bacteria.other.count, 
                                     data.bacteria.unique, 
                                     by='bacteria_code')
  setorder(data.bacteria.other.count, -N)
  head(data.bacteria.other.count, 10)
  nrow(data.bacteria.other.count)
  setnames(data.bacteria.other.count, column.other, "other")
  plot <- ggplot(data.bacteria.other.count[0:8], aes(x = reorder(paste(bacteria,
                                                                       other,
                                                                       sep = ' + '),-N), 
                                                     y = N)) + 
    geom_bar(stat="identity") + 
    theme_bw() + 
    xlab('pair') + 
    ylab('count') + 
    theme(text = element_text(size=13), 
          axis.text.x = element_text(angle=10, vjust=1))
  setnames(data.bacteria.other.count, "other", column.other)
  return(list(plot=plot, data.bacteria.other.count=data.bacteria.other.count))
}

GetBacteria <- function(raw.sentences){
  data.bacteria <- raw.sentences[bacteria != '',
                                 .(unlist(llply(strsplit(unlist(strsplit(bacteria, ', ')), ';'), 
                                                .fun=function(x) x[1])),
                                   unlist(llply(strsplit(unlist(strsplit(bacteria, ', ')), ';'), 
                                                .fun=function(x) x[2]))),
                                 by=.(text, article_title, journal)]
  setnames(data.bacteria, c("text","article_title", "journal", "bacteria","bacteria_code"))
  data.bacteria
}

GetBacteriaNutrientDiseaseFood <- function(raw.sentences){
  data.bacteria <- GetBacteria(raw.sentences)
  
  data.nutrient <- raw.sentences[nutrients != '',
                                 .(unlist(llply(strsplit(unlist(strsplit(nutrients, ', ')), ';'), 
                                                .fun=function(x) x[1])),
                                   unlist(llply(strsplit(unlist(strsplit(nutrients, ', ')), ';'), 
                                                .fun=function(x) x[2]))),
                        by=.(text, article_title, journal)]
  setnames(data.nutrient, c("text","article_title", "journal", "nutrient_name", "nutrient"))
  
  data.disease <- raw.sentences[diseases!='',.(unlist(llply(strsplit(unlist(strsplit(diseases, ', ')), ';'), 
                                                            .fun=function(x) x[1])),
                                               unlist(llply(strsplit(unlist(strsplit(diseases, ', ')), ';'), 
                                                            .fun=function(x) x[2]))),
                                by=.(text, article_title, journal)]
  setnames(data.disease, c("text","article_title", "journal", "disease","disease_code"))
  
  data.food <- raw.sentences[food!='',.(tolower(unlist(llply(str_match_all(food, 
                                                          '(\\w+);'), 
                                            .fun=function(x) x[,2]))),
                       unlist(llply(str_match_all(food, 
                                                  ';([\\w ]+)'), 
                                    .fun=function(x) x[,2]))),
                    by=.(text, article_title, journal)]
  setnames(data.food, c("text","article_title","journal","food","foodgroup"))
  
  return(list(bacteria = data.bacteria, nutrient = data.nutrient, disease = data.disease, food = data.food))
}


GetBacteriaNutrientDiseaseFoodOldFormat <- function(raw.sentences){
  data.bacteria <- raw.sentences[,
                        .(unlist(llply(str_match_all(bacteria, '\'([^\\)]+)\''), .fun=function(x) x[,2])),
                          unlist(llply(str_match_all(bacteria, '(\\d+)\\)'), .fun=function(x) x[,2]))),
                        by=.(text, article_title, journal)]
  setnames(data.bacteria, c("text","article_title", "journal", "bacteria","bacteria_code"))

  data.nutrient <- raw.sentences[,
                        unlist(llply(str_match_all(nutrients, ',\\s\'([^\\)]+)\''), .fun=function(x) x[,2])),
                        by=.(text, article_title, journal)]
  setnames(data.nutrient, c("text","article_title", "journal", "nutrient"))

  data.disease <- raw.sentences[,.(unlist(llply(str_match_all(diseases,
                                                     '\'([^\\)]+)\','),
                                       .fun=function(x) x[,2])),
                          unlist(llply(str_match_all(diseases,
                                                     ',\\s\'([^\\)]+)\''),
                                       .fun=function(x) x[,2]))),
                       by=.(text, article_title, journal)]
  setnames(data.disease, c("text","article_title", "journal", "disease","disease_code"))

  data.food <- raw.sentences[,.(tolower(unlist(llply(str_match_all(food,
                                                          '\'([^\\)]+)\','),
                                            .fun=function(x) x[,2]))),
                       unlist(llply(str_match_all(food,
                                                  ',\\s\'([^\\)]+)\''),
                                    .fun=function(x) x[,2]))),
                    by=.(text, article_title, journal)]
  setnames(data.food, c("text","article_title","journal","food","foodgroup"))

  return(list(bacteria = data.bacteria, nutrient = data.nutrient, disease = data.disease, food = data.food))
}


CleanBacteriaData <- function(data.bacteria){
  # data.bacteria.catalog <- fread("../data/bacteria/gut_catalog.csv")
  # data.bacteria <- data.bacteria[bacteria_code %in% data.bacteria.catalog$id]
  data.bacteria <- data.bacteria[bacteria_code != 562] # no E. coli
  data.bacteria <- data.bacteria[bacteria_code != 1496] # no Clostridium difficile
  data.bacteria <- data.bacteria[bacteria_code != 590] # no Salmonella
  data.bacteria
}

CleanFoodData <- function(data.food){
  data.food <- data.food[food != "water"]
  data.food <- data.food[food != "pie"]
  data.food <- data.food[food != "bf"]
  data.food
}