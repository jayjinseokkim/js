


# evaluating embeddings.

import numpy as np
from gensim.matutils import unitvec

def test(model,positive,negative,test_words):

  mean = []
  for pos_word in positive:
    mean.append(1.0 * np.array(model[pos_word]))

  for neg_word in negative:
    mean.append(-1.0 * np.array(model[neg_word]))

  # compute the weighted average of all words
  mean = unitvec(np.array(mean).mean(axis=0))

  scores = {}
  for word in test_words:

    if word not in positive + negative:

      test_word = unitvec(np.array(model[word]))

      # Cosine Similarity
      scores[word] = np.dot(test_word, mean)

  print(sorted(scores, key=scores.get, reverse=True)[:10]) #1





## js
from gensim.models import Word2Vec
model = Word2Vec.load('wiki.en.word2vec.model')

positive_words = ["samsung","usa"]

negative_words = ["korea"]

# Test Word2vec
print("Testing Word2vec")
#model = word2vec.getModel()
test(model,positive_words,negative_words,model.wv.vocab)

# # Test Fasttext
# print("Testing Fasttext")
# model = fasttxt.getModel()
# test(model,positive_words,negative_words,model.words)





positive_words = ["redundant"]

negative_words = []

# Test Word2vec
print("Testing Word2vec")
#model = word2vec.getModel()
test(model,positive_words,negative_words,model.wv.vocab)




#tensorboard monitor.

#due to pdf extract issue.
tpage = open('firstsample.txt', 'r').read()


tpage = tpage.decode('utf-8')
tpage = tpage.lower()


# In[12]:

brknm = ['deutsche bank', 'bank of america', 'reuters','bloomberg','exchange','bnp','paribas'
         ,'ticker','market','markets','research','company','update']
    
for nm in brknm:
    tpage = re.sub(nm, '', tpage, flags=re.I)


# In[13]:

seplist =[]
#seplist.append('Important Disclosures')
seplist.append('disclaimers and disclosures')  ## better be lowercase.

for sep in seplist:
  tpage = tpage.split(sep, 1)[0]
