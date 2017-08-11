from gensim.corpora import WikiCorpus

language_code = "en"
inp = 'D:/torrent/enwiki-latest-pages-articles-multistream.xml.bz2'
outp = "wiki.{}.text".format(language_code)
i = 0

print("Starting to create wiki corpus")
#output = open(outp, 'w')
output = open(outp, 'w', encoding = 'UTF-8')
space = " "
wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
for text in wiki.get_texts():
  article = space.join([t.decode("utf-8") for t in text])

  output.write(article + "\n")
  i = i + 1
  if (i % 5000 == 0):
    print("Saved " + str(i) + " articles")

 # if (i == 20000):
 # 	break

output.close()
print("Finished - Saved " + str(i) + " articles")




import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import time

language_code = "en"
inp = "wiki.{}.text".format(language_code)
out_model = "wiki.{}.word2vec.model".format(language_code)
size = 300   #or 800d
window = 5
min_count = 5

start = time.time()

model = Word2Vec(LineSentence(inp), sg = 1, # 0=CBOW , 1= SkipGram
	     size=size, window=window, min_count=min_count, workers=multiprocessing.cpu_count())

# trim unneeded model memory = use (much) less RAM
model.init_sims(replace=False) #True

print(time.time()-start)

model.save(out_model)
	
