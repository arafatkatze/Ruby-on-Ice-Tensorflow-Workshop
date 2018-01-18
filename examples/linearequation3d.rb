require 'tensorflow'
graph = Tensorflow::Graph.new
tensor_1 = Tensorflow::Tensor.new([[1.0, 1.0, -1],
                                    [1, -2, 3],
                                    [2, 3, 1]])
tensor_2 = Tensorflow::Tensor.new([[4.0],
                                    [-6.0],
                                    [7]])
'''
Consider the equations
x + y - z = 4
x -2y +3z =-6
2x +3y + z = 7
'''
placeholder_1 = graph.placeholder('tensor1', tensor_1.type_num)
placeholder_2 = graph.placeholder('tensor2', tensor_2.type_num)
opspec = Tensorflow::OpSpec.new('MatrixSolve', 'MatrixSolve', nil, [placeholder_1, placeholder_2])
op = graph.AddOperation(opspec)
session_op = Tensorflow::Session_options.new
session = Tensorflow::Session.new(graph, session_op)
hash = { placeholder_1 => tensor_1, placeholder_2 => tensor_2 }
result = session.run(hash, [op.output(0)], [])
print result[0], "\n"
'''
The solution of the equations is
x = 1
y = 2
z = -0.99  (almost -1)
'''