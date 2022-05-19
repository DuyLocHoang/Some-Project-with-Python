import pandas as pd
import numpy as np
import sklearn
from sklearn import model_selection,linear_model
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

data = pd.read_csv('dataset/student/student-mat.csv',sep = ';')
print(data.head())
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
print(data.head(5))

predict = 'G3'

X = np.array(data.drop([predict],1))
y = np.array(data[predict])
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.1)
#Train model
best = 0
for _ in range(30):
    X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.1)
    linear = linear_model.LinearRegression()
    linear.fit(X_train,y_train)
    acc = linear.score(X_test, y_test)
    print(acc)
    if acc > best :
        best = acc
        #Save model
        with open('linearmodel.pickle','wb') as f :
            pickle.dump(linear,f)
#Load model
linear = open('linearmodel.pickle', 'rb')
linear = pickle.load(linear)
print(linear.score(X_test,y_test))
print('Cof: ',linear.coef_)
print('intercept: ',linear.intercept_)

#Predict
predictions = linear.predict(X_test)
for i in range(len(X_test)) :
    print(predictions[i],X_test[i],y_test[i] )

#Drawing data
plot = 'G1'
plt.scatter(data[plot],data['G3'])
plt.xlabel(plot)
plt.ylabel('Final Grade')
plt.show()