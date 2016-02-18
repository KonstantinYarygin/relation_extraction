setwd('/home/konstantin/documents/projects/python/text_mining/relation_extraction/analysis')
rm(list=ls())

bacteria <- read.table('bacteria.csv', sep='\t', header=F)
colnames(bacteria) <- c('bacterium', 'count')
nutrients <- read.table('nutrients.csv', sep='\t', header=F)
colnames(nutrients) <- c('nutrient', 'count')
diseases <- read.table('diseases.csv', sep='\t', header=F)
colnames(diseases) <- c('disease', 'count')
bacteria_nutrients_pairs <- read.table('bacteria_nutrients_pairs.csv', sep='\t', header=F)
colnames(bacteria_nutrients_pairs) <- c('bacterium', 'nutrient', 'count')
nutrients_diseases_pairs <- read.table('nutrients_diseases_pairs.csv', sep='\t', header=F)
colnames(nutrients_diseases_pairs) <- c('nutrient', 'disease', 'count')
diseases_bacteria_pairs <- read.table('diseases_bacteria_pairs.csv', sep='\t', header=F)
colnames(diseases_bacteria_pairs) <- c('disease', 'bacterium', 'count')

head(bacteria, 10)
head(nutrients, 10)
head(diseases, 10)
head(bacteria_nutrients_pairs, 10)
head(nutrients_diseases_pairs, 10)
head(diseases_bacteria_pairs, 10)


library(reshape)
library(gplots)
library(RColorBrewer)
cols.gentleman <- function(ncol=500) {
    hmcol <- colorRampPalette(brewer.pal(10, 'RdBu'))(ncol)
    return(rev(hmcol))
}

ccc <- cast(diseases_bacteria_pairs, bacterium~disease, fill=0)
rownames(ccc) <- ccc$bacterium
ccc$bacterium <- NULL
ccc <- ccc[apply(ccc, 1, sum) > 100, apply(ccc, 2, sum) > 100]
pdf('diseases_bacteria_1.pdf', 8, 8)
heatmap.2(data.matrix(apply(ccc, 2, function(x) x/sum(x))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()
pdf('diseases_bacteria_2.pdf', 8, 8)
heatmap.2(t(data.matrix(apply(ccc, 1, function(x) x/sum(x)))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()


ccc <- cast(bacteria_nutrients_pairs, bacterium~nutrient, fill=0)
rownames(ccc) <- ccc$bacterium
ccc$bacterium <- NULL
ccc <- ccc[apply(ccc, 1, sum) > 30, apply(ccc, 2, sum) > 30]
pdf('bacteria_nutrients_1.pdf', 8, 8)
heatmap.2(data.matrix(apply(ccc, 2, function(x) x/sum(x))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()
pdf('bacteria_nutrients_2.pdf', 8, 8)
heatmap.2(t(data.matrix(apply(ccc, 1, function(x) x/sum(x)))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()

ccc <- cast(nutrients_diseases_pairs, disease~nutrient, fill=0)
rownames(ccc) <- ccc$disease
ccc$disease <- NULL
ccc <- ccc[apply(ccc, 1, sum) > 10, apply(ccc, 2, sum) >10]
pdf('disease_nutrients_1.pdf', 8, 8)
heatmap.2(data.matrix(apply(ccc, 2, function(x) x/sum(x))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()
pdf('disease_nutrients_2.pdf', 8, 8)
heatmap.2(t(data.matrix(apply(ccc, 1, function(x) x/sum(x)))),
          Rowv=FALSE,
          Colv=FALSE,
          labRow = rownames(ccc),
          labCol = colnames(ccc),
          dendrogram="none",
          col=cols.gentleman(500), cexRow=1, cexCol=1,
          trace='none', scale="none", keysize=1,
          lmat=rbind(c(4,3,0),c(2,1,0), c(0,0,0)),
          lwid=c(0.1,2,0.5),lhei=c(0.1,2,0.4)
          )
dev.off()

