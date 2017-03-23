
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


# setup a TensorFlow session
tf.reset_default_graph()
sess = tf.InteractiveSession()
X = tf.Variable([0.0], name='embedding')
place = tf.placeholder(tf.float32, shape=embedding.shape)
set_x = tf.assign(X, place, validate_shape=False)
sess.run(tf.global_variables_initializer())
sess.run(set_x, feed_dict={place: embedding})

# write labels
with open('log2/metadata.tsv', 'w') as f:
    for word in lab:
        f.write(word + '\n')

# create a TensorFlow summary writer
summary_writer = tf.summary.FileWriter('log2', sess.graph)
config = projector.ProjectorConfig()
embedding_conf = config.embeddings.add()
embedding_conf.tensor_name = 'embedding:0'
embedding_conf.metadata_path = os.path.join('log2', 'metadata.tsv')
projector.visualize_embeddings(summary_writer, config)

# save the model
saver = tf.train.Saver()
saver.save(sess, os.path.join('log2', "model.ckpt"))

tensorboard --logdir log2  ## this one is correct.

