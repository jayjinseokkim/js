
library(tm) #corpus
library(stringi) #stri_trans_tolower
library(stringr) #str_extract
library(xlsx) #read.xlsx
library(data.table)
library(dplyr) #mutate_each
library(reshape) #to use melt() in ggplot
library(grid)
library(ggplot2)
library(gtable)

############ setup ################
rm(list=setdiff(ls(), "first_docs"))
#data load
docs <- Corpus(DirSource("./DB"), readerControl = list(reader=readPDF()))
first_docs <- docs
docs <- first_docs
sTime = proc.time() #check running time
#set pdf format : single=0, bundle=1
#set split string if pdf_format is bundle
pdf_format <- 0
#set range : day=0, week=1, month=2
range <- 2
#how to get date : from title=0, from pdf=1
get_date <- 0
#remove unnecessary word #1
for(i in 1:length(docs)) {
  docs[[i]]$content <- gsub("[^a-zA-Z0-9]"," ", docs[[i]]$content)  
}
#set date
if(get_date==0) {
  #get date from title
  for(i in 1:length(docs)) {
    meta(docs[[i]],"datetimestamp") <- str_extract(docs[[i]]$meta$id,"\\d{2}\\d{2}\\d{4}")
    meta(docs[[i]],"datetimestamp") <- as.Date(meta(docs[[i]],"datetimestamp"), format = "%m%d%Y")
  }
}
#remove unnecessary words #2
docs <- tm_map(docs, removeWords, stopwords("SMART"))
docs <- tm_map(docs, removeWords, stopwords("english"))
docs <- tm_map(docs, content_transformer(stri_trans_tolower))
docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, stripWhitespace)
#set date list
######################################################
mat <- new.env()
for(i in 1:length(docs)) {
  id <- str_sub(docs[[i]]$meta$id, 12, 16)
  ext <- sapply(strsplit(id, "\\."), `[[`, 1)
  aa <- c("US")
  final_id <- paste(ext, aa)
  mat <- rbind(mat, final_id) 
  i <- i+1
}

for(i in 1:length(docs)) {
  if(i==1) {
    date <- docs[[i]]$meta$datetimestamp
    title <- docs[[i]]$meta$id
    tckr <- mat[i]
  }
  else{
    date <- append(date,docs[[i]]$meta$datetimestamp)
    title <- append(title,docs[[i]]$meta$id)
    tckr <- append(tckr,mat[i])
  }
}
######################################################
#set week list
week <- as.Date(paste(stri_sub(format(date, "%Y-%V"),1,4),
                      as.numeric(stri_sub(format(date, "%Y-%V"),-2,-1))*7, sep =" "), format = "%Y %j")
#set month list
month <- as.Date(paste(format(date, "%Y-%m"), "-01",sep="")) 
############# DATA PREPROCESSING END #############
#diction <- as.data.table(read.csv(file.choose()))
diction <- as.data.table(read.csv("./LoughranMcDonald_MasterDictionary_2014.csv"))
diction <- mutate_each(diction, funs(tolower))
diction.m <- as.matrix(diction)  #to use 'for'loop, change to matrix
diction.m <- diction.m[, c(1,8:14)] #extract necessary column
###

AGG <- NULL ; AGG2 <- NULL

naming = c("neg","pos","unc","lit","con","sup","int")
#naming[1]

for( i in 1:7 ) {
  
  colnm = naming[i]
  senti.v <- as.vector(diction.m[diction.m[,i+1]>0 , 1])
  
  #polysemous
  if(i==3) {#uncertainty
    senti.v = senti.v[!(senti.v=="may")]
  }
  
  sDTM <- DocumentTermMatrix(docs, list(dictionary=senti.v))
  
  
  # infer subject.
  j = 64
  docs[[j]]$meta$id
  TESTM <- DocumentTermMatrix(docs[j])
  freq <- sort(colSums(as.matrix(TESTM)), decreasing = TRUE)
  head(freq,30)
  #maxterms <- apply(TESTM, 1, which.max)
  #TESTM$dimnames$Terms[maxterms]
  #TESTMM <- as.matrix(TESTM)
  #TESTV  <- sort(rowSums(TESTMM), decreasing = TRUE)
  #head(TESTV, 1)
  # infer subject. end.
  
    
  ap.m <- as.matrix(sDTM)
  ap.v <- rowSums(ap.m) #sum of word which present sentiment
  
  #make table daily/weekly/monthly
  if(range==0) {
    #sum by day
    ap.d <- data.table(date, ap.v)
  }else if(range==1) {
    #sum by week
    ap.d <- data.table(date, ap.v)
  }else if(range==2) {
    ap.d <- data.table(date, ap.v)  ##id = title, tckr, date, senti=ap.v
  }
  colnames(ap.d) <- c("date", colnm)
  setkey(ap.d, date)

  tempcol <- ap.d[[ncol(ap.d)]]
    
  # ap.d <- ap.d[,sum(senti), by=id]
  
  if(i==1) {
    AGG <- ap.d
  }else{
  #  unique_keys <- unique(c(AGG[,date], ap.d[,date]))    ##    unique_keys <- unique(c(AGG[,id], ap.d[,id]))

    AGG = data.table(AGG, tempcol)   ##    AGG <- AGG[ap.d[J(unique_keys)],allow.cartesian=TRUE]
    colnames(AGG)[colnames(AGG) =="tempcol"  ] <- colnm
  }
  
}

#setnames(AGG, c("Date","neg","pos","unc","lit","con","sup","int"))
#setnames(AGG, c("Ticker","Date","neg2","neg","pos2","pos","unc2","unc","lit2","lit","con2","con","sup2","sup","int2","int"))
write.csv(AGG, file = "AGG_check.csv")
# create sentiment table by (firm / date range / autor)
AGG2 <- AGG
AGG2$total = with(AGG2, neg+pos+unc+lit+con+sup+int)
#AGG2$total = with(AGG2, neg2+pos2+unc2+lit2+con2+sup2+int2)
# threshold
AGG2 <- AGG2[total > 50, ]
AGG2$neg <-  AGG2$neg / AGG2$total
AGG2$pos <-  AGG2$pos / AGG2$total
AGG2$unc <-  AGG2$unc / AGG2$total
AGG2$lit <-  AGG2$lit / AGG2$total
AGG2$con <-  AGG2$con / AGG2$total
AGG2$sup <-  AGG2$sup / AGG2$total
AGG2$int <-  AGG2$int / AGG2$total


