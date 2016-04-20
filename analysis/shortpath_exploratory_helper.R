PlotHist <- function(data, variable, title, max=10, scale.f=NULL){
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
  if (!is.null(scale.f)) {
    plot <- plot + geom_text(aes(label=scale.f * percent/100), position=position_dodge(0.9), vjust=1.25)
  }
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

GetDeleteTemplates <- function(){
  template.bact <- c('species', 'spp', 'strain', 'strains', 'specie', 'BACTERIUM', 'OTU', 'members','member', 
                     'phylum','phylums', 'class', 'classes','order', 'orders', 'family',
                     'families', 'genus', 'genuses', 'members', 'member','microbiota', 
                     'microbiom', 'bacteria', 'bacterium', 'community', 'communities', 'pathogen', 'pathogens')
  template.samples <- c('patient', 'patients', 'child', 'children', 'subject','subjects','cohort', 'cohorts',
                        'site','sites', 'counts', 'count','group', 'groups', 'samples',
                        'sample', 'genus', 'genuses', 'members', 'member','microbiota', 
                        'microbiom', 'bacteria', 'bacterium', 'community', 'communities')
  template.disease <- c('DISEASE', 'disease', 'diseases', 'infection', 'infections')
  template.verbs <- c('considered',  'consider', 'considers', 'considering', 'observe', 'observes', 'observed', 'observing', 
                      'find',  'found',  'finds',  'finding', 'report', 'reports', 'reported', 'reporting', 
                      'development', 'corresponding', 'suffering', 'shown')	
  template.delete <- c(template.bact, template.samples, template.disease, template.verbs)
  template.delete
}

DeleteWords <- function(data.graph, template.delete){
  data.graph$words <- lapply(data.graph$words, function(x) {x[(x %in% template.delete)]})
  data.graph$length <- lapply(data.graph$words, length)
  data.graph
}

ReadGraphData <- function(path){
  data <- fread(path, col.names = c('text', 'length', 'from', 'to', 
                         'fromtag', 'totag', 'path', 'tags', 
                         'allwords', 'alltags', 'graph'))
}

PrepareWordsAndPhrases <- function(data.graph){
  data.graph$words <- strsplit(data.graph$path, "', '", fixed=T)
  data.graph$words <- sapply(data.graph$words, tolower)
  data.graph$phrase <- sapply(data.graph$words, 
                              function(x) {ifelse(length(x)>2, paste(x[2:(length(x)-1)], collapse=' '), '')})
  data.graph$phrase <- tolower(data.graph$phrase)
  data.graph
}