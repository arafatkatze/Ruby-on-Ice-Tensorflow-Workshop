require 'matrix'
brainweight = []
bodyweight  = []
File.readlines('data/regression_data.txt').each do |line|
    words = line.split(',')
    brainweight.push(words[0].to_f)
    bodyweight.push(words[1].to_f)
end
ones_array = Array.new(brainweight.size,1) 
X_matrix = Matrix[ones_array, brainweight].transpose
Y_matrix = Matrix[bodyweight].transpose
X_matrix_Transpose = X_matrix.transpose
X_matrix_pseudo_inverse = (X_matrix_Transpose*X_matrix).inverse * X_matrix_Transpose
Beta = X_matrix_pseudo_inverse * Y_matrix
print Beta, "\n"
