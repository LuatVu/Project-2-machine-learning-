#kich thuoc hien tai cua van ban la 347

import network2
import network_evaluation # dung de danh gia
import cPickle as cp
import numpy as np
import matplotlib.pyplot as pls

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


input_file_training_data = "/home/luat/Desktop/ML/Training_data.txt"
input_file_validation_data = "/home/luat/Desktop/ML/Validation_Data.txt"
input_file_test_data = "/home/luat/Desktop/ML/Test_Data.txt"

def vectorization(j):
	e = np.zeros( (7,1) )
	e[j] = 1.0
	return e


# open file training data--------------------------------------------------------
File = open(input_file_training_data, "r")
training_data = cp.load(File)
File.close()


input_data = []
output_data = []

# vector hoa x, va y 
for x, y in training_data:
	input_data.append(x)
	output_data.append(y)
X = [np.reshape(x, (347,1)) for x in input_data]
Y = [vectorization(y) for y in output_data]

training_data = zip(X,Y)


# open file validation data---------------------------------------------------------------

File = open(input_file_validation_data,'r')
validation_data = cp.load(File)
File.close()

input_data = []
output_data = []

# vector hoa x, con y thi giu nguyen (khong can vector hoa y boi de de cho qua trinh danh gia)
for x, y in validation_data:
	input_data.append(x)
	output_data.append(y)
X = [np.reshape(x, (347,1) ) for x in input_data ]

validation_data = zip(X, output_data)




# open file test data-------------------------------------------------------------------------------
File = open(input_file_validation_data,'r')
test_data = cp.load(File)
File.close()

input_data = []
output_data = []

# vector hoa x, con y thi giu nguyen (khong can vector hoa y boi de de cho qua trinh danh gia)
for x, y in test_data:
	input_data.append(x)
	output_data.append(y)
X = [np.reshape(x, (347,1) ) for x in input_data ]

test_data = zip(X, output_data)
#-------------------------------------------------------------------------------------------------------------------


# xay dung mang neural================================================================
net = network2.Network( [347, 20, 7], cost = network2.CrossEntropyCost )

e_cost = []
e_accuracy = []
train_cost = []
train_accuracy = []


net_evaluation = network_evaluation.Network( [347, 100, 7], cost = network_evaluation.CrossEntropyCost )

e_cost_2 = []
e_accuracy_2 = []
train_cost_2 = []
train_accuracy_2 = []



def run(eta, lamda): # eta = 0.01, lmbda = 5.0
	global e_cost, e_accuracy, train_cost, train_accuracy
	e_cost , e_accuracy, train_cost, train_accuracy = \
	net.SGD(training_data, 100, 10, eta, lmbda = lamda, evaluation_data=validation_data, monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True, monitor_training_cost=True)

def run_2(eta, lamda):
	global e_cost_2, e_accuracy_2, train_cost_2, train_accuracy_2
	e_cost_2 , e_accuracy_2, train_cost_2, train_accuracy_2 = \
	net_evaluation.SGD(training_data, 100, 10, eta, lmbda = lamda, evaluation_data=validation_data, monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True, monitor_training_cost=True)

def plotCostGraph(number):
	x = [i for i in range(1, len(e_cost) + 1 )] 
	pls.plot(x, e_cost,'r')
	pls.plot(x, train_cost,'b')
	pls.title("The graph compares between using (cross entropy, small weight initialize) and (quadratic , gaussian weight initilize)")
	pls.xlabel("Epoch")
	pls.ylabel("Cost function value")
	pls.legend(["evaluation cost","training cost"],loc= number)
	pls.show()

def plotAccurateGraph(number):
	x = [i for i in range(1, len(e_accuracy) + 1)]
	pls.plot(x, e_accuracy,'r')
	pls.plot(x, train_accuracy, 'b')
	pls.title("The graph of accurate evaluation")
	pls.xlabel("Epoch")
	pls.ylabel("Accuracy")
	pls.legend(["accurate of evaluated data","accurate of training data"],loc=number)
	pls.show()

# dau vao se la 1 vector bat ki, dau ra se la mot nhan lien quan toi chu de van ban.
def label(vector):
	label = np.argmax(vector)
	if(label == 0):
		return "Phap Luat"
	elif (label == 1):
		return "Kinh Doanh"
	elif (label == 2):
		return "The Thao"
	elif (label == 3):
		return "Suc Khoe"
	elif (label == 4):
		return "Giao Duc"
	elif (label == 5):
		return "Khoa Hoc"
	else:
		return "Xe"

# dau vao la duong dan cua mot van ban can phan loai (van ban nay khong duoc gan nhan), dau ra se la ten van ban
def classify(net,inputFile):
	File = open(inputFile, "r")
	data = cp.load(File)
	File.close()
	x = np.reshape(data , (347,1))
	vector = net.feedforward(x)
	return label(vector)



def y_testdata_y_predict(input_File_Network, input_File_Test_Data):
	Net = network2.load(input_File_Network)
	file = open(input_File_Test_Data,'r')
	data = cp.load(file)
	file.close()
	y_test =[]
	y_predict = []
	for x, y in data:
		y = vectorization(y).tolist()
		x = np.reshape(x, (347,1) )
		y_test.append(y)
		y_predict.append( vectorization(  np.argmax(Net.feedforward(x) ) ).tolist() )
	return y_test, y_predict


def evaluation(y_test, y_predict):
	precision = []
	recall = []
	f1 = []
	for i in range(0,7):
		y = []
		y_pre = []
		
		for j in range(0,len(y_test) ):
			y.append(y_test[j][i])
			y_pre.append(y_predict[j][i])

		precision.append( precision_score(y, y_pre, average='binary') )
		recall.append( recall_score(y, y_pre, average='binary') )
		f1.append( f1_score(y, y_pre, average='binary') )
	return precision, recall, f1
