from __future__ import print_function
import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import numpy as np
import collections
import math
import random
import pandas
import argparse
from sklearn import metrics
import sys


#Tensorflow TfLearn
learn = tf.contrib.learn

#SocketIO init
batch_size = 24
EMBEDDING_SIZE = 128
n_words = 0
max_seq_length = 20

tf.logging.set_verbosity(tf.logging.ERROR)


#embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))

vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(max_seq_length)



def read_and_split_dataset(filename_train,filename_test):
	#Reading Data
	fields = ['label','data']
	dataset = pandas.read_csv(filename_train,header=None)
	x_train = pandas.DataFrame(dataset)[1]
	y_train = pandas.DataFrame(dataset)[0]
	
	dataset_test = pandas.read_csv(filename_test,header=None)
	x_test  = pandas.DataFrame(dataset_test)[1]
	y_test = pandas.DataFrame(dataset_test)[0]

	
	dataset_test_input = pandas.read_csv("test.csv",header=None)
	input_data = pandas.DataFrame(dataset_test_input)[0]

	


	#Creating Lexicon

	
	x_train = np.array(list(vocab_processor.fit_transform(x_train)))
	x_test = np.array(list(vocab_processor.transform(x_test)))
	input_data = np.array(list(vocab_processor.transform(input_data)))
	n_words = len(vocab_processor.vocabulary_)
	


	return x_train,y_train,x_test,y_test,n_words


def convert_input_vector(sentence):
	sentences= [sentence]
	
	sentences = np.array((list(vocab_processor.transform(sentences))))
	#print(sentences)
	return sentences



def rnn_model(features, target):
  """RNN model to predict from sequence of words to a class."""
  # Convert indexes of words into embeddings.
  # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
  # maps word indexes of the sequence into [batch_size, sequence_length,
  # EMBEDDING_SIZE].



  word_vectors = tf.contrib.layers.embed_sequence(
      features, vocab_size=n_words, embed_dim=EMBEDDING_SIZE, scope='words')

  # Split into list of embedding per word, while removing doc length dim.
  # word_list results to be a list of tensors [batch_size, EMBEDDING_SIZE].
  word_list = tf.unstack(word_vectors, axis=1)
  

  # Create a Gated Recurrent Unit cell with hidden size of EMBEDDING_SIZE.
  cell =  tf.nn.rnn_cell.GRUCell(EMBEDDING_SIZE)

  # Create an unrolled Recurrent Neural Networks to length of
  # MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit.
  _, encoding =tf.nn.rnn(cell, word_list, dtype=tf.float32)

  # Given encoding of RNN, take encoding of last step (e.g hidden size of the
  # neural network of last step) and pass it as features for logistic
  # regression over output classes.


  target = tf.one_hot(target, 6, 1, 0)
  logits = tf.contrib.layers.fully_connected(encoding, 6, activation_fn=None)
  loss = tf.contrib.losses.softmax_cross_entropy(logits, target)

  # Create a training op.
  train_op = tf.contrib.layers.optimize_loss(
      loss,
      tf.contrib.framework.get_global_step(),
      optimizer='Adam',
      learning_rate=0.01)


  return ({
      'class': tf.argmax(logits, 1),
      'prob': tf.nn.softmax(logits)
  }, loss, train_op)


def main(mode,input_data):
	
	global n_words
	
	x_train , y_train , x_test, y_test,n_words = read_and_split_dataset("input.csv","input_test.csv")
	
	# Build model
	model_fn = rnn_model
	
	if mode == "train":
		
		classifier = learn.Estimator(model_fn=model_fn,model_dir="ckpt")
		# Train and predict
		classifier.fit(x_train, y_train, steps=None ,max_steps=100)


		y_predicted = [p['class'] for p in classifier.predict(x_test, as_iterable=True)]
		score = metrics.accuracy_score(y_test, y_predicted)
		print('Accuracy: {0:f}'.format(score))	
	
	if mode =="test":
		classifier = learn.Estimator(model_fn=model_fn,model_dir="ckpt")
		#classifier.fit(x_train, y_train,max_steps=100)
		input_data2 = convert_input_vector(input_data)
		print(input_data2)
		classifier.evaluate(x_test,y_test)
		predicted = [p['class'] for p in classifier.predict(input_data2, as_iterable=True)]
		print(predicted[0])
		return predicted[0]
		



#main("train","wake me up at 5 pm")


	

