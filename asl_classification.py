# -*- coding: utf-8 -*-
"""ASL_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Yp4v0nKdBgfAUBSUKuZqOfbp2MmqdWTj
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import tensorflow as tf
import numpy as np
import glob
import matplotlib.pyplot as plt
import kaggle
from skimage import transform # pip install scikit-image

#physical_devices = tf.config.experimental.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], True)

"""## 1. Load dataset, explore it and split it into train, validation and test sets

If you are running this tutorial locally such as in vsCode, download the dataset in the link below, unzip, and save in a new local folder called /asl-alphabet. 

### Larger dataset
https://www.kaggle.com/datasets/grassknoted/asl-alphabet

### Smaller dataset
https://www.kaggle.com/datasets/danrasband/asl-alphabet-test

If running this tutorial google colab, follow this link (https://www.analyticsvidhya.com/blog/2021/06/how-to-load-kaggle-datasets-directly-into-google-colab/) to download an api key kaggle.json file from your kaggle acount and uncomment and the following code to download the dataset directly from kaggle.
"""

# Code for downloading the dataset directly from Kaggle in Google Colab using unique api key
! pip install -q kaggle # Install kaggle
! mkdir ~/.kaggle # Make a new .kaggle directory
! echo '{"username":"tysontrail","key":"29decad2f17556a9de6abf9e5b93dc21"}' > ~/.kaggle/kaggle.json #write kaggle API credentials to kaggle.json
! chmod 600 ~/.kaggle # Change the permissions of the file
! mkdir asl_alphabet # Create new directory 

# uncomment for larger dataset
! kaggle datasets download -d grassknoted/asl-alphabet # Download dataset from kaggle
! unzip -q asl-alphabet.zip -d asl_alphabet/ # Unzip and save in newly created directory

# uncomment for smaller dataset
# ! kaggle datasets download -d danrasband/asl-alphabet-test # Download dataset from kaggle
# ! unzip -q asl-alphabet-test.zip -d asl_alphabet/ # Unzip and save in newly created directory
# ! rm -r asl_alphabet/asl-alphabet-test # Remove additional unneccessary duplicate library

# Create class names
class_names = ["A", "B", "C", "D", "E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","del","nothing","space"]

# Specify image output folder
IMG_OUT = "./output_images/"

# Save images as array 
# images = np.asarray(glob.glob("asl_alphabet/asl_alphabet_train/asl_alphabet_train" + "/*/*.jpg"))
images = np.asarray(glob.glob("asl_alphabet/asl_alphabet_train/asl_alphabet_train" + "/*/*.jpg"))

# Save labels as array
labels = np.asarray([f.split("/")[-2] for f in images])

print(len(images))
print(images[:50])
print(labels[:50])

# Representing class names as integers
Y = np.zeros(len(labels))
for ii in range(len(class_names)):
    Y[labels == class_names[ii]] =  ii

# Dimensions we will resize the images
img_height = 224
img_width = 224

# X = np.empty((len(images), img_height, img_width, 3))
# X[:] = [np.resize(plt.imread(img), (img_height, img_width, 3)) for img in images]

# Robertos code from class - Python for loop slows down computations
X = np.zeros((len(images),img_height,img_width,3))
for (ii,img) in enumerate(images):
    X[ii] = transform.resize(plt.imread(img),(img_height,img_width,3))

# Displaying some samples from the development set
sample_indexes = np.random.choice(np.arange(X.shape[0], dtype = int),size = 30, replace = False)
plt.figure(figsize = (24,18))
for (ii,jj) in enumerate(sample_indexes):
    plt.subplot(5,6,ii+1)
    plt.imshow(X[jj], cmap = "gray")
    plt.title("Label: %s" %class_names[int(Y[jj])])
plt.savefig(IMG_OUT + "dev_set_samples.png")
plt.close()
# plt.show()

#The number of classes across samples looks balanced
# Let's shuffle the samples and split them
indexes = np.arange(X.shape[0], dtype = int)
np.random.shuffle(indexes)
X = X[indexes]*255
print(X.shape)

#X = tf.keras.applications.mobilenet.preprocess_input(X)
Y = Y[indexes]

# Train/validation/test split
nsplit1 = int(0.75*X.shape[0]) 
nsplit2 = int(0.9*X.shape[0]) 
# Train and validation split

X_train = X[:nsplit1]
Y_train = Y[:nsplit1]

X_val = X[nsplit1:nsplit2]
Y_val = Y[nsplit1:nsplit2]

X_test = X[nsplit2:]
Y_test = Y[nsplit2:]

print("\nTrain set")
print("Images: ",X_train.shape)
print("Labels shape: ",Y_train.shape)

print("\nValidation set")
print("Images: ",X_val.shape)
print("Labels shape: ",Y_val.shape)

print("\nTest set")
print("Images: ",X_test.shape)
print("Labels shape: ",Y_test.shape)

"""## 2. Data Scaling"""

# Scaling RBG channel values from [0,255] to [-1,1] for MobileNet model
X_train = (X_train / 127.5) - 1.0
X_val = (X_val / 127.5) - 1.0
X_test = (X_test / 127.5) - 1.0

"""## 3. One hot encoding"""

Y_train_oh = tf.keras.utils.to_categorical(Y_train)
Y_val_oh = tf.keras.utils.to_categorical(Y_val)
Y_test_oh = tf.keras.utils.to_categorical(Y_test)

print("Labels:")
print(Y_train[:29])
print()
print("One hot encoded labels:")
print(Y_train_oh[:29])

"""## 4. Define your callbacks (save your model, patience, etc.)"""

model_name = "asl_classifier_cnn.h5"
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience = 20)

monitor = tf.keras.callbacks.ModelCheckpoint(model_name, monitor='val_loss',\
                                             verbose=0,save_best_only=True,\
                                             save_weights_only=False,\
                                             mode='min')
# Learning rate schedule
def scheduler(epoch, lr):
    if epoch%4 == 0 and epoch!= 0:
        lr = lr/2
    return lr

lr_schedule = tf.keras.callbacks.LearningRateScheduler(scheduler,verbose = 0)

"""## 5. Keras Data Augmentation"""

batch_size = 32
gen_params = {"featurewise_center":False,"samplewise_center":False,"featurewise_std_normalization":False,\
              "samplewise_std_normalization":False,"zca_whitening":False,"rotation_range":20,"width_shift_range":0.1,"height_shift_range":0.1,\
              "shear_range":0.2, "zoom_range":0.1,"horizontal_flip":True,"fill_mode":'constant',\
               "cval": 0}
train_gen = tf.keras.preprocessing.image.ImageDataGenerator(**gen_params, preprocessing_function = tf.keras.applications.mobilenet.preprocess_input)
val_gen = tf.keras.preprocessing.image.ImageDataGenerator(**gen_params, preprocessing_function = tf.keras.applications.mobilenet.preprocess_input)

train_gen.fit(X_train,seed = 1)
val_gen.fit(X_val, seed = 1)

train_flow = train_gen.flow(X_train,Y_train_oh,batch_size = batch_size)
val_flow = val_gen.flow(X_val,Y_val_oh,batch_size = batch_size)

# Displaying some samples from the development set
plt.figure(figsize = (32,24))
Xbatch,Ybatch = train_flow.__getitem__(0)
print(Xbatch.mean(),Xbatch.std())
print(Xbatch.min(),Xbatch.max())
for ii in range(batch_size):
    plt.subplot(7,5,ii+1)
    plt.imshow((Xbatch[ii]- Xbatch[ii].min())/(Xbatch.max() - Xbatch[ii].min()), cmap = "gray")
    plt.title("Label: %s" %class_names[int(Ybatch[ii].argmax())])
# plt.show()
plt.savefig(IMG_OUT + "augmented_set.png")
plt.close()

"""## 6. Transfer Learning
6.1 Choose and load your pretrained model without the top (i.e., the prediction part, usually the fully connected layers)

6.2 Freeze the layers (i.e., make them non-trainable) of your pretrained model
"""

base_model = tf.keras.applications.MobileNet(
    weights='imagenet',  # Load weights pre-trained on ImageNet.
    input_shape=(img_height, img_width, 3),
    include_top=False) 
base_model.trainable = False

"""6.3. Add a top (i.e., the prediction layers)"""

#input_image = tf.keras.Input(shape=(img_height, img_width, 3))
x1 = base_model(base_model.input, training = False)
x2 = tf.keras.layers.Flatten()(x1)
out = tf.keras.layers.Dense(len(class_names),activation = 'softmax')(x2)
model = tf.keras.Model(inputs = base_model.input, outputs =out)
print(model.summary())

model.compile(optimizer=tf.keras.optimizers.Adam(lr = 1e-4),
              loss='categorical_crossentropy',
              metrics=['accuracy'])


model.fit(train_flow,epochs = 5, \
          verbose = 1, callbacks= [early_stop, monitor, lr_schedule],validation_data=(val_flow))

# model = tf.keras.models.load_model(model_name)
# model.trainable = True

# model.compile(optimizer=tf.keras.optimizers.Adam(lr = 1e-8),
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
# print(model.summary())
# model.fit(train_flow, epochs = 5, \
#           verbose = 1, callbacks= [early_stop, monitor, lr_schedule],validation_data=(val_flow))

X_test = tf.keras.applications.mobilenet.preprocess_input(X_test)
model.load_weights(model_name)
metrics = model.evaluate(X_test,Y_test_oh)

# Investigating correct labelling
Ypred = model.predict(X_test).argmax(axis = 1)
right_indexes = np.where(Ypred == Y_test)[0]

# Displaying some samples from the development set
sample_indexes_right = np.random.choice(np.arange(right_indexes.shape[0], dtype = int),size = 30, replace = True)
plt.figure(figsize = (24,18))
for (ii,jj) in enumerate(sample_indexes_right):
    plt.subplot(5,6,ii+1)
    aux = X_test[right_indexes[jj]]
    aux = (aux - aux.min())/(aux.max() - aux.min())
    plt.imshow(aux, cmap = "gray")
    plt.title("Label: %d, predicted: %d" %(Y_test[right_indexes[jj]],Ypred[right_indexes[jj]]))
# plt.show()
plt.savefig(IMG_OUT + "correctly_labelled.png")
plt.close()

#Investigating incorrect labelling
wrong_indexes = np.where(Ypred != Y_test)[0]

# Displaying some samples from the development set
sample_indexes = np.random.choice(np.arange(wrong_indexes.shape[0], dtype = int),size = 30, replace = False)
plt.figure(figsize = (24,18))
for (ii,jj) in enumerate(sample_indexes):
    plt.subplot(5,6,ii+1)
    aux = X_test[wrong_indexes[jj]]
    aux = (aux - aux.min())/(aux.max() - aux.min())
    plt.imshow(aux, cmap = "gray")
    plt.title("Label: %d, predicted: %d" %(Y_test[wrong_indexes[jj]],Ypred[wrong_indexes[jj]]))
# plt.show()
plt.savefig(IMG_OUT + "incorrectly_labelled.png")
plt.close()

