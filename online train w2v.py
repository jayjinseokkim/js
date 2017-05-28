import os
import glob
from time import time
import json

sentences = ""
text = ""
start = time()
i = 0

#fb 702_20170405063215/702_webhose-2017-03_20170405063221
#   711_20170405070700\711_webhose-2017-03_20170405070703
#   705_20170405065304\705_webhose-2017-03_20170405065308
#   708_20170405070014\708_webhose-2017-03_20170405070017
path = 'C:/Users/jins_desktop/Downloads/702_20170405063215/702_webhose-2017-03_20170405063221'
for filename in glob.glob(os.path.join(path, '*.json')):
  with open(filename, 'rt', encoding='UTF8') as data_file:
    for line in data_file:
      json_line = json.loads(line)
      text = json_line['text']
      sentences = sentences + "\n" +text
  i = i + 1
  if (i % 1000 == 0):
    print("Saved " + str(i) + " articles")
  if (i == 5000000):    ## as ceiling.
    break
print('took %.2f seconds to run.' %(time()-start))

with open("online_train_textdata_702", "w", encoding = 'UTF-8') as text_file:
  print(sentences, file = text_file)
sentences = ""


from gensim.corpora import WikiCorpus
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

start = time()
model = Word2Vec.load("wiki.en.word2vec.model_702")
inp = "online_train_textdata_708"
model.train(LineSentence(inp))
out_model = "wiki.en.word2vec.model_708"
model.save(out_model)
print('took %.2f seconds to train.' %(time()-start))
