import sklearn
from sklearn import model_selection,svm
from sklearn import datasets
from sklearn import metrics
# Load data
cancer = datasets.load_breast_cancer()

print(cancer.feature_names)
print(cancer.target_names)
classes = ['malignant' 'benign']
X = cancer.data
y = cancer.target
print(X.shape, y.shape)

X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.2)

model = svm.SVC(kernel='linear',C = 2)
model.fit(X_train,y_train)
predictions = model.predict(X_test)
acc= metrics.accuracy_score(y_test,predictions)
print(acc)

