#!/usr/bin/python3 -i
'''
A very simple MNIST classifier.
See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
'''
import argparse
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

def plotImage(data, idx, pred=-1):
	arr1 = data.images[idx,:]
	in_dim = np.sqrt(arr1.shape[0]).astype(int)
	arr2 = arr1.reshape((in_dim,in_dim))
	plt.ion()
	plt.figure()
	plt.pcolor(arr2)
	plt.xlim((0,in_dim))
	plt.xticks([])
	plt.xlabel('true: '+str(data.labels[idx].argmax()), fontsize=25)
	plt.ylim((0,in_dim))
	plt.gca().invert_yaxis()
	plt.yticks([])
	if pred>=0 and pred<10:
		plt.title('pred: '+str(pred), fontsize=25)
	plt.tight_layout()

def load_and_train(options):
	# load data and define parameters
	mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
	in_dim = np.sqrt(mnist.train.images.shape[1]).astype(int)
	num_of_train, out_dim = mnist.train.labels.shape
	
	# construst the model
	x = tf.placeholder(tf.float32, [None, in_dim*in_dim])
	W = tf.Variable(tf.zeros([in_dim*in_dim, out_dim]))
	b = tf.Variable(tf.zeros([1,out_dim]))
	h = tf.nn.softmax( tf.matmul(x, W) + b )
	
	# supervise with known labels
	y = tf.placeholder(tf.float32, [None, out_dim])
	
	# define loss function
	cross_entropy = tf.reduce_mean( -tf.reduce_sum( tf.log(h)*y, reduction_indices=[1] ) )
	correct_prediction = tf.equal( tf.argmax(h,1), tf.argmax(y,1) )
	accuracy = tf.reduce_mean( tf.cast(correct_prediction, tf.float32) )
	train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
	
	# init and train
	with tf.Session() as sess:
		tf.initialize_all_variables().run()
		for idx in range(options.train_steps):
			batch_xs, batch_ys = mnist.train.next_batch(options.batch_size)
			sess.run(train_step, feed_dict={x:batch_xs, y:batch_ys})
			# test the current model
			print('step', idx, 'acc:', accuracy.eval({x: batch_xs, y: batch_ys}), 'epoch:', mnist.train.epochs_completed)
	
		# evaluate the final results
		results = tf.argmax(h,1).eval({x:mnist.test.images})
	# return test set for evaluation
	return (mnist.test, results)

def build_options():
	parser = argparse.ArgumentParser()
	parser.add_argument('--batch-size', type=int,
		dest='batch_size', help='number of digit images to be feeded at one time',
		metavar='BATCH_SIZE', default=220)
	parser.add_argument('--train-steps', type=int,
		dest='train_steps', help='total number of steps in training, reset when one epoch is completed',
		metavar='TRAIN_STEPS', default=2000)
	return parser.parse_args()

# main function
if __name__ == '__main__':
	options = build_options()
	xys, hs = load_and_train(options)
