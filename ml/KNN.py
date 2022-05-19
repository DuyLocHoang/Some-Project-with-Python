import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn import linear_model,preprocessing,model_selection
import pickle

# Load data
data = pd.read_csv('dataset/car.data')
print(data.head(5))

# data non-numberic -> numberic
le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data['buying']))
maint = le.fit_transform(list(data['maint']))
door = le.fit_transform(list(data['door']))
persons = le.fit_transform(list(data['persons']))
lug_boot = le.fit_transform(list(data['lug_boot']))
safety = le.fit_transform(list(data['safety']))
cls = le.fit_transform(list(data['class']))
# print(buying)

X = list(zip(buying,maint,door,persons,lug_boot,safety))
y = list(cls)
# print(X)

X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.1)

# Train model KNN

model = KNeighborsClassifier(7)
model.fit(X_train,y_train)
with open('knnmodel.pickle','wb') as f:
    pickle.dump(model,f)

print(model.score(X_test,y_test))

predictions = model.predict(X_test)

names = ["unacc", "acc", "good", "vgood"]
for i in range(len(predictions)):
    print('Predictions:',names[predictions[i]],'X test: ',X_test[i],'Actual: ',names[y_test[i]])
    n = model.kneighbors([X_test[i]],7,True)
    print(n)
# Look at neighbors



