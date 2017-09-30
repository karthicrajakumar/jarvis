import MySQLdb
import pandas


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="delta2345",  # your password
                     db="jarvis")        # name of the data bases


cur = db.cursor()


#dataset = pandas.read_csv("input.csv",header=None)
#x_train = pandas.DataFrame(dataset)[1]
#y_train = pandas.DataFrame(dataset)[0]
	
dataset_test = pandas.read_csv("input_test.csv",header=None)
x_train  = pandas.DataFrame(dataset_test)[1]
y_train = pandas.DataFrame(dataset_test)[0]

	
dataset_test_input = pandas.read_csv("test.csv",header=None)
input_data = pandas.DataFrame(dataset_test_input)[0]


for i in range(len(x_train)):
	print(y_train[i], x_train[i])
	cur.execute("INSERT into `jarvis`.`testing_data` (`label`,`testing_data`) values(%s,%s)"	,(y_train[i],x_train[i]))



db.commit()