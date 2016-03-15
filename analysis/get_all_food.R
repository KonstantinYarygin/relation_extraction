library(data.table)
library(stringr)
library(stringdist)

FOOD_DES_PATH = '~/do/relation_extraction/data/food/sr28asc/FOOD_DES.txt'
FOOD_GROUP_PATH = '~/do/relation_extraction/data/food/sr28asc/FD_GROUP.txt'
OUTPUT_FILE_NAME = 'food.tsv'

data <- fread(FOOD_DES_PATH, sep="^")
setnames(data, c("NDB_No", "FdGrp_Cd", "Long_Desc", "Shrt_Desc", "ComName", "ManufacName", "Survey", "Ref_desc", "Refuse", "SciName", "N_Factor", "Pro_Factor", "Fat_Factor", "CHO_Factor"))

data$Long_Desc <- gsub("~", "", data$Long_Desc)
data$Shrt_Desc <- gsub("~", "", data$Shrt_Desc)
data$SciName <- gsub("~", "", data$SciName)
data$FdGrp_Cd <- gsub("~", "", data$FdGrp_Cd)

# take first words
data[,long_begin:=gsub(pattern = ",\\s.*$", replacement = "", x = Long_Desc)]
data[,short_begin:=gsub(pattern = ",.*$", replacement = "", x = Shrt_Desc)]

# load group info, attach group name
data.group <- fread(FOOD_GROUP_PATH, sep="^", header=FALSE)
setnames(data.group, c("FdGrp_Cd", "FdGrp_Desc"))
data.group$FdGrp_Cd <- gsub("~", "", data.group$FdGrp_Cd)
data.group$FdGrp_Desc <- gsub("~", "", data.group$FdGrp_Desc)

data <- merge(data, data.group, by='FdGrp_Cd')
data[,long_begin:=tolower(long_begin)]
data[,short_begin:=tolower(short_begin)]

data.sub <- unique(data[,.(long_begin, short_begin, SciName, FdGrp_Desc)])
data.sub[,long_begin:=tolower(long_begin)]
data.sub[,short_begin:=tolower(short_begin)]
data.sub[,SciName:=tolower(SciName)]
# remove abbreviations (similar strings) from short descriptions
data.similar <- stringdist(data.sub$long_begin, 
                           data.sub$short_begin, method="jw") < 0.2
data.sub[data.similar, short_begin:=""]
data.sub <- unique(data.sub)

data.sub.words1 <- data.sub[long_begin!="",.(unique(long_begin)),by=.(FdGrp_Desc)]
data.sub.words2 <- data.sub[short_begin!="",.(unique(short_begin)),by=.(FdGrp_Desc)]
data.sub.words3 <- data.sub[SciName!="",.(unique(SciName)),by=.(FdGrp_Desc)]

data.sub.plain <- rbind(data.sub.words1, data.sub.words2, data.sub.words3)
setnames(data.sub.plain, c("group", "word"))
setorder(data.sub.plain, group)

write.table(data.sub.plain, OUTPUT_FILE_NAME, sep="\t", row.names = FALSE, quote = FALSE)
