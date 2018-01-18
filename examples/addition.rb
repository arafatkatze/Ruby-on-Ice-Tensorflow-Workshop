require 'tensorflow'
graph = Tensorflow::Graph.new
tensor_1 = Tensorflow::Tensor.new([[1.0, 3.0, 5.0], [2.0, 4.0, 7.0]])
tensor_2 = Tensorflow::Tensor.new([[-5.0, 1.2, 4.5], [8.0, 2.3, 3.1]])
# print tensor_1.shape, " \n", tensor_1.element_type, "\n", tensor_1.rank, "\n"
placeholder_1 = graph.placeholder('tensor1', tensor_1.type_num)
placeholder_2 = graph.placeholder('tensor2', tensor_2.type_num)
opspec = Tensorflow::OpSpec.new('Addition_of_tensors', 'Add', nil, [placeholder_1, placeholder_2])
op = graph.AddOperation(opspec)
session_op = Tensorflow::Session_options.new
session = Tensorflow::Session.new(graph, session_op)
hash = { placeholder_1 => tensor_1, placeholder_2 => tensor_2 }
result = session.run(hash, [op.output(0)], [])
print result[0], "\n"
graph.write_file("protobuf.pb")
