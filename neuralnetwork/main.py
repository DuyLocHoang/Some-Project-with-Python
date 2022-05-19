import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images,train_labels),(test_images,test_labels) = data.load_data()
# print(len(np.unique(train_labels)))
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print(train_images.shape)
train_images = train_images/255.0
test_images = test_images/255.0

# plt.imshow(train_images[1],cmap =plt.cm.binary )
# plt.show()

#Create model
model = keras.Sequential([
    keras.layers.Flatten(input_shape = (28,28)),
    keras.layers.Dense(128,activation = 'relu'),
    keras.layers.Dense(10,activation = 'softmax')
    ])
model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy',metrics = ['accuracy'])
model.fit(train_images,train_labels,epochs = 5)

test_loss,test_acc = model.evaluate(test_images,test_labels)
print("Tested acc: ",test_acc)

predictions = model.predict(test_images)

for i in range(5):
    plt.imshow(test_images[i],cmap = plt.cm.binary)
    plt.xlabel("Actual: " + class_names[test_labels[i]])
    plt.title("Predictions: " + class_names[np.argmax(predictions[i])])
    plt.show()