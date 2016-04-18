PlotHist <- function(data, variable, title, max=10){
  setnames(data, variable, "object")
  plot <- ggplot(data[0:max], aes(x = reorder(object, -percent), y = percent)) + 
    geom_bar(stat='identity', width=.5, fill=rgb(0.6, 0.6, 0.6, alpha=0.7)) + 
    theme_bw() +
    xlab(variable) +
    ylab('% of all sentences in subset') + 
    ggtitle(title) +
    geom_text(aes(label=round(percent, 2)), position=position_dodge(width=0.9), vjust=-0.25) +
    theme(text = element_text(size=13), 
          axis.text.x = element_text(angle=10, vjust=1))
  setnames(data, "object", variable)
  plot
}

GetWordsAndTags <- function(data, words.number){
  #words parsing
  if (is.na(words.number)){
    data[,.(strsplit(path, "', '", fixed=T))]
    words <- strsplit(data$path, "', '", fixed=T)
    tags <- strsplit(data$tags, "', '", fixed=T)
  } else {
    words <- strsplit(data[length==words.number+2]$path, "', '", fixed=T)
    tags <- strsplit(data[length==words.number+2]$tags, "', '", fixed=T)
  }
  words <- unlist(lapply(words, function(x) {x[-c(1, length(x))]}))
  words <- tolower(words)
  #tags parsing
  tags <- unlist(lapply(tags, function(x) {x[-c(1, length(x))]}))
  words.tags <- data.table(cbind(words, tags))
  setnames(words.tags, c("word", "tag"))
  words.tags
}
GetStat <- function(words, tags.to.match){
  tags.to.match.str <- paste(tags.to.match, collapse="|")
  words.match <- words[as.vector(!(is.na(str_match(tag, tags.to.match.str))))]
  words.match <- words.match[, .N/nrow(words.match)*100, by=word]#
  names(words.match) <- c('word', 'percent')
  setorder(words.match, -percent)
  words.match
}
GetTagStat <- function(words){
  tags <- data.table(tag=words[!(tag %in% c("DISEASE", "BACTERIUM"))]$tag)
  tags.num <- tags[, .N/nrow(words)*100, by=tag]
  names(tags.num) <- c('tag', 'percent')
  tags.num <- merge(tags.num, tag.abbs, by=c('tag'), all.x=T)
  tags.num <- tags.num[order(-percent)]
  tags.num
}