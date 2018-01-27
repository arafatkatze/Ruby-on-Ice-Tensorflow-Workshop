# This file is useful for converting protobuf files generated by ruby
# so that they can be used by tensorboard.
# The resulting files are created in a directory specified in
# directory variable below. You can specify the directory by changing the directory
# variable. You also have to specify the source protobuf file which
# you will be using.
# Once you convert the protobuf file using this file.
# You can use the command given below as an example to run Tensorboard.
# Example if the directory is /home/arafat/Desktop/test
# tensorboard --logdir=/home/arafat/Desktop/test

import tensorflow as tf
import shutil
import os
import sys
from google.protobuf import text_format
from tensorflow.python.platform import gfile

def pbtxt_to_board(filename, directory):
    with open(filename, 'r') as f:
        graph_def = tf.GraphDef()
        file_content = f.read()
        text_format.Merge(file_content, graph_def)
        tf.import_graph_def(graph_def, name='')
        tf.summary.FileWriter(directory, graph_def=graph_defination)


def graphdef_to_board(filename, directory):
    with gfile.FastGFile(filename, 'rb') as f:
        graph_defination = tf.GraphDef()
        graph_defination.ParseFromString(f.read())
        tf.import_graph_def(graph_defination, name='')
        tf.summary.FileWriter(directory, graph_def=graph_defination)
    return


# A simple check to remove the directory if its already present.
if sys.argv[1]:
    directory = sys.argv[1]
else:
    directory = "/home/arafat/Desktop/test"
# if (os.path.isdir(directory)):
#    shutil.rmtree(directory)

# Name of the file to be converted
filename = 'a.pb'
graphdef_to_board(filename, directory)
