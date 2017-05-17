

import os
import glob
from time import time
import json

sentences = []
text = []
start = time()

path = 'C:/Users/jins_desktop/Downloads/702_20170405063215/702_webhose-2017-03_20170405063221'
for filename in glob.glob(os.path.join(path, '*.json')):
  with open(filename, 'rt', encoding='UTF8') as data_file:
    for line in data_file:
      json_line = json.loads(line)
      text = json_line['text']
      sentences.append(text)
print('took %.2f seconds to run.' %(time()-start))


model = Word2Vec.load("wiki.en.word2vec.model")
model.train(sentences)
out_model = "wiki.en.word2vec.model_0517"
model.save(out_model)

