data.journals <- data.table(read.delim('title_journal_impact.tsv', sep='\t', header = FALSE))
data.journals <- unique(data.journals)
setnames(data.journals, c("article_title", "journal", "impact"))
data.sentences <- fread('sentences_first.csv')
setkey(data.sentences, 'article_title')
setkey(data.journals, 'article_title')
data.merged <- merge(data.sentences, data.journals[,.(article_title, journal)], all.x = TRUE)

write.csv(data.merged, file = "sentences_first_with_journals.csv", row.names=FALSE)
