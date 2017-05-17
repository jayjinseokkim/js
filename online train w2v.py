

import os
import glob
from time import time
import json

sentences = []
text = []
start = time()
i = 0

path = 'C:/Users/jins_desktop/Downloads/702_20170405063215/702_webhose-2017-03_20170405063221'
for filename in glob.glob(os.path.join(path, '*.json')):
  with open(filename, 'rt', encoding='UTF8') as data_file:
    for line in data_file:
      json_line = json.loads(line)
      text = json_line['text']
      sentences.append(text)
  i = i + 1
  if (i % 10000 == 0):
    print("Saved " + str(i) + " articles")
  if (i == 300000):    ## as ceiling.
    break
print('took %.2f seconds to run.' %(time()-start))


start = time()
model = Word2Vec.load("wiki.en.word2vec.model")
model.train(sentences)
out_model = "wiki.en.word2vec.model_0517"
model.save(out_model)
print('took %.2f seconds to train.' %(time()-start))
