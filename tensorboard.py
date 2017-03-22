
############## tensorboard visualization
import os
import tensorflow as tf
import numpy as np
#import fasttext
from tensorflow.contrib.tensorboard.plugins import projector

# load model
#word2vec = fasttext.load_model('wiki.en.bin')

# create a list of vectors
embedding = np.empty((len(visual), 300), dtype=np.float32)
for i in range(len(visual)):
  embedding[i] = visual[i]


