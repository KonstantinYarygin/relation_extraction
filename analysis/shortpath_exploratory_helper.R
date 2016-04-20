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

GetWordsAndTags <- function(data){
  ExcludeLastAndFirst <- function (x) {x[-c(1, length(x))]}
  words <- data[,.(strsplit(path, "', '", fixed=T), strsplit(tags, "', '", fixed=T), text)]
  words <- words[,.(unlist(lapply(V1, ExcludeLastAndFirst)), unlist(lapply(V2, ExcludeLastAndFirst))), by=text]
  setnames(words, c("text", "word", "tag"))
  words$word <- tolower(words$word)
  words
}
GetStat <- function(words, tags.to.match){
  tags.to.match.str <- paste(tags.to.match, collapse="|")
  words.match <- words[as.vector(!(is.na(str_match(tag, tags.to.match.str))))]
  words.match.text <- unique(words.match[, .(.N/nrow(words.match)*100, text), by=word])
  setnames(words.match.text, c('word', 'percent', 'text'))
  setorder(words.match.text, -percent)
  words.match <- unique(words.match.text[,.(word, percent)])
  return(list(words.match=words.match, words.match.text=words.match.text))
}
GetTagStat <- function(words){
  tags <- data.table(tag=words[!(tag %in% c("DISEASE", "BACTERIUM"))]$tag)
  tags.num <- tags[, .N/nrow(words)*100, by=tag]
  names(tags.num) <- c('tag', 'percent')
  tags.num <- merge(tags.num, tag.abbs, by=c('tag'), all.x=T)
  tags.num <- tags.num[order(-percent)]
  tags.num
}