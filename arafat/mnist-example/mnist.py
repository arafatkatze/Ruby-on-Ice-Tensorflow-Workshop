
#images tab
#image summary 

#still haven't seen audio example in TF 
#magenta is a good example 

#graph tab
#name scopes as squares
#direction of arrows shows the direction tensors are flowing
#placeholder x shows entrypoint for data 
#to reduce clutter TB shows node connected to many others nodes in there own section in detail
#we could add and remove to main graph if we wanted to
#we could see the values at each time step if we wanted to 
#we can see either which structure are being used or which devices each oeration is running on 
#we could manually upload a saved TF graph right from the UI if we'd like 
#the graph detects structures that are the exact same and colors them the same , unless its grey thats just default
#we can see how many tensors inside the lines
#more name scopes, the more abstraction, simpler the graph

#distributions
#to visualize the distributions of activations coming off a particular layer, or the distribution of gradients or weights.

#histogram
#The histogram plot allows you to plot variables from your graph.
#So if you're model has  weights, the histogram shows how the values of those weights change with training.

#embeddings
#PCA vs T-SNE
#The idea of SNE and t-SNE is to place neighbors close to each other, (almost) completly ignoring the global structure.
#PCA is quite the opposite. It tries to preserve the global properties (eigenvectors with high variance) while it may lose low-variance deviations between neighbors.
#http://stats.stackexchange.com/questions/238538/are-there-cases-where-pca-is-more-suitable-than-t-sne/249520#249520
#can also load training weights
#find neighbors
#share finding
#need moar plugins
#You can also construct custom specialized linear projections based on text searches for finding meaningful directions in space. 


import os
import os.path
import shutil
import tensorflow as tf

LOGDIR = "/tmp/mnist_tutorial/"
LABELS = os.path.join(os.getcwd(), "labels_1024.tsv")
SPRITES = os.path.join(os.getcwd(), "sprite_1024.png")
### MNIST EMBEDDINGS ###
#downloads and reads the data
#The MNIST data is split into three parts: 55,000 data points of training data (mnist.train), 10,000 points of test data (mnist.test), and 5,000 points of validation data (mnist.validation).
#very MNIST data point has two parts: an image of a handwritten digit and a corresponding label. We'll call the images "x" and the labels "y".
#Each image is 28 pixels by 28 pixels. We can interpret this as a big array of numbers:
#https://www.tensorflow.org/images/MNIST-Matrix.png
mnist = tf.contrib.learn.datasets.mnist.read_data_sets(train_dir=LOGDIR + "data", one_hot=True)
### Get a sprite and labels file for the embedding projector ###
#If you have images associated with your embeddings, you will need to produce a single image consisting of
# small thumbnails of each data point. This is known as the sprite image. The sprite should have the same number 
#of rows and columns with thumbnails stored in row-first order: the first data point placed in the 
#top left and the last data point in the bottom right:
#TSV is a file extension for a tab-delimited file used with spreadsheet software. 
#TSV stands for Tab Separated Values. TSV files are used for raw data and can be 
#imported into and exported from spreadsheet software.
### Get a sprite and labels file for the embedding projector ###

if not (os.path.isfile(LABELS) and os.path.isfile(SPRITES)):
  print("Necessary data files were not found. Run this command from inside the "
    "repo provided at "
    "https://github.com/dandelionmane/tf-dev-summit-tensorboard-tutorial.")
  exit(1)


#first we'll define layers as re-usable functions

#Typically, a CNN is composed of a stack of convolutional modules that perform feature extraction. 
#Each module consists of a convolutional layer followed by a pooling layer. The last convolutional module 
#is followed by one or more dense layers that perform classification. The final dense layer in a CNN contains 
#a single node for each target class in the model (all the possible classes the model may predict), with a 
#Softmax Activation to generate value between 0 and 1 for each node
#is equal to 1). We can interpret the softmax values for a given image as relative measurements of how likel
#it is that the image falls into each target class.
#Summary - tensor flow op that outputs protocol buffers
#Scalar summary - single value  (line charts) 
#Image summary (visualize images) generative
#Audio
#Histogram (see dsitbrutiuons of values ) weights 
#Tensor (any kind) in development
# we can merge them all at the end

def conv_layer(input, size_in, size_out, name="conv"):
  with tf.name_scope(name):
    #tf.name_scope creates namespace for operators in the default graph, places into group, easier to read
    #A graph maintains a stack of name scopes. A `with name_scope(...):`
    #statement pushes a new name onto the stack for the lifetime of the contextself.
    #Ops have names, name scopes group ops
    
    w = tf.Variable(tf.truncated_normal([5, 5, size_in, size_out], stddev=0.1), name="W")
    #A variable maintains state in the graph across calls to run(). You add a variable to the graph by constructing an instance of the class Variable.
    #truncated normal Outputs random values from a truncated normal distribution.
    b = tf.Variable(tf.constant(0.1, shape=[size_out]), name="B")
    #constant Creates a constant tensor.
   
    conv = tf.nn.conv2d(input, w, strides=[1, 1, 1, 1], padding="SAME")
    #Computes a 2-D convolution given 4-D input and filter tensors.
    #1 Flattens the filter to a 2-D matrix
    #2 Extracts image patches from the input tensor to form a virtual tensor
    #3 For each patch, right-multiplies the filter matrix and the image patch vector.

    act = tf.nn.relu(conv + b)
    #nonlin relu reduces likelihood of vanishing gradient, most used activation function these days

    tf.summary.histogram("weights", w)
    tf.summary.histogram("biases", b)
    tf.summary.histogram("activations", act)
    return tf.nn.max_pool(act, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    #Let's say we have an 4x4 matrix representing our initial input. 
    #Let's say as well that we have a 2x2 filter that we'll run over our input. 
    #We'll have a stride of 2 (meaning the (dx, dy) for stepping over our input will be (2, 2)) and won't overlap regions.
    #For each of the regions represented by the filter, we will take the max of that region and create a new, output matrix 
    #where each element is the max of a region in the original input.
    # It's like taking a flash light to find out the most useful features of an image.

#Dense (fully connected) layers perform classification on the 
#features extracted by the convolutional layers and downsampled by the 
#pooling layers. In a dense layer, every node in the layer is connected to every node in the preceding layer.
# Add fully connected layer
def fc_layer(input, size_in, size_out, name="fc"):
  with tf.name_scope(name):
    w = tf.Variable(tf.truncated_normal([size_in, size_out], stddev=0.1), name="W")
    b = tf.Variable(tf.constant(0.1, shape=[size_out]), name="B")
    act = tf.matmul(input, w) + b
    tf.summary.histogram("weights", w)
    tf.summary.histogram("biases", b)
    tf.summary.histogram("activations", act)
    return act


def mnist_model(learning_rate, use_two_fc, use_two_conv, hparam):
  tf.reset_default_graph()
  sess = tf.Session()

  # Setup placeholders, and reshape the data
  x = tf.placeholder(tf.float32, shape=[None, 784], name="x")
  x_image = tf.reshape(x, [-1, 28, 28, 1]) 
  # The pixel Dimensions of the image
  # This is a 4-dimensional Data
  tf.summary.image('input', x_image, 3)
  # Summary to be used for Tensorboard
  y = tf.placeholder(tf.float32, shape=[None, 10], name="labels")
  #The Placeholder for labels

  if use_two_conv:
    conv1 = conv_layer(x_image, 1, 32, "conv1")
    conv_out = conv_layer(conv1, 32, 64, "conv2")
    
  else:
    conv1 = conv_layer(x_image, 1, 64, "conv")
    conv_out = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

  flattened = tf.reshape(conv_out, [-1, 7 * 7 * 64])
  #We can flatten this array into a vector of 28x28 = 784 numbers. 
  #It doesn't matter how we flatten the array, as long as we're consistent 
  #between images. From this perspective, the MNIST images are just a bunch of 
  #points in a 784-dimensional vector space, with a very rich structure 

  if use_two_fc:
    fc1 = fc_layer(flattened, 7 * 7 * 64, 1024, "fc1")
    relu = tf.nn.relu(fc1)
    embedding_input = relu
    tf.summary.histogram("fc1/relu", relu)
    embedding_size = 1024
    #logits the sum of the inputs may not equal 1, that the values are not probabilities
    #we'll feed these to the last (softmax) to make them probabilities
    logits = fc_layer(fc1, 1024, 10, "fc2")
  else:
    embedding_input = flattened
    embedding_size = 7*7*64
    logits = fc_layer(flattened, 7*7*64, 10, "fc")

  with tf.name_scope("xent"):
    #Computes the mean of elements across dimensions of a tensor.
    #so in this case across output probabilties
    xent = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(
            logits=logits, labels=y), name="xent")
    tf.summary.scalar("xent", xent)

  with tf.name_scope("train"):
    #Adam offers several advantages over the simple tf.train.GradientDescentOptimizer. 
    #Foremost is that it uses moving averages of the parameters (momentum); 
    #This enables Adam to use a larger effective step size, and the algorithm will converge to this step size without fine tuning.
    #The main down side of the algorithm is that Adam requires more computation to be performed for each parameter 
    #in each training step (to maintain the moving averages and variance, and calculate the scaled gradient); 
    #and more state to be retained for each parameter (approximately tripling the size of the model to store the average and variance for each parameter). 
    #A simple tf.train.GradientDescentOptimizer could equally be used in your MLP,
    #but would require more hyperparameter tuning before it would converge as quickly.
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(xent)

  with tf.name_scope("accuracy"):
    #Returns the index with the largest value across axes of a tensor.
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
    #Casts a tensor to a new type.
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar("accuracy", accuracy)

  #merge them all so one write to disk, more comp efficient
  summ = tf.summary.merge_all()

  #intiialize embedding matrix as 0s
  embedding = tf.Variable(tf.zeros([1024, embedding_size]), name="test_embedding")
  #give it calculated embedding
  assignment = embedding.assign(embedding_input)
  #initialize the saver
# Add ops to save and restore all the variables.
  saver = tf.train.Saver()

  sess.run(tf.global_variables_initializer())
  writer = tf.summary.FileWriter(LOGDIR + hparam)
  writer.add_graph(sess.graph)

  config = tf.contrib.tensorboard.plugins.projector.ProjectorConfig()
  embedding_config = config.embeddings.add()
  embedding_config.tensor_name = embedding.name
  embedding_config.sprite.image_path = SPRITES
  embedding_config.metadata_path = LABELS
  # Specify the width and height of a single thumbnail.
  embedding_config.sprite.single_image_dim.extend([28, 28])
  tf.contrib.tensorboard.plugins.projector.visualize_embeddings(writer, config)

  for i in range(2001):
    batch = mnist.train.next_batch(100)
    if i % 5 == 0:
      [train_accuracy, s] = sess.run([accuracy, summ], feed_dict={x: batch[0], y: batch[1]})
      writer.add_summary(s, i)
    if i % 500 == 0:
      sess.run(assignment, feed_dict={x: mnist.test.images[:1024], y: mnist.test.labels[:1024]})
      saver.save(sess, os.path.join(LOGDIR, "model.ckpt"), i)
    sess.run(train_step, feed_dict={x: batch[0], y: batch[1]})

def make_hparam_string(learning_rate, use_two_fc, use_two_conv):
  conv_param = "conv=2" if use_two_conv else "conv=1"
  fc_param = "fc=2" if use_two_fc else "fc=1"
  return "lr_%.0E,%s,%s" % (learning_rate, conv_param, fc_param)

def main():
  # You can try adding some more learning rates
  for learning_rate in [1E-3, 1E-4]:

    # Include "False" as a value to try different model architectures
    for use_two_fc in [True]:
      for use_two_conv in [False, True]:
        # Construct a hyperparameter string for each one (example: "lr_1E-3,fc=2,conv=2")
        hparam = make_hparam_string(learning_rate, use_two_fc, use_two_conv)
        print('Starting run for %s' % hparam)

        # Actually run with the new settings
        mnist_model(learning_rate, use_two_fc, use_two_conv, hparam)
  print('Done training!')
  print('Run `tensorboard --logdir=%s` to see the results.' % LOGDIR)
  print('Running on mac? If you want to get rid of the dialogue asking to give '
        'network permissions to TensorBoard, you can provide this flag: '
        '--host=localhost')

if __name__ == '__main__':
  main()
