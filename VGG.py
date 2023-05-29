import tensorflow as tf
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.optimizers import Adam
import read_data
import os

dr = read_data.DataReader()
dr.f_data_reader((128,128))


# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), input_shape = (128,128,3),activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2000, activation=tf.nn.relu),
    tf.keras.layers.Dense(5, activation=tf.nn.softmax)
])

# Compile the model
model.compile(optimizer=Adam(lr=0.001), metrics=['accuracy'], loss='sparse_categorical_crossentropy')

print("model defined\n\n", model.summary())

print("\n\n************ TRAINING START ************")
early_stop = EarlyStopping(monitor='val_loss', patience=4)
early_stop2 = EarlyStopping(monitor='val_accuracy', patience=4)
print(dr.y_train.dtype)

#checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=os.path('./trained_models/lane_navigation_check3.h5'), verbose=1, save_best_only=True)

history = model.fit(dr.x_train, dr.y_train, epochs=30, batch_size=32,
                    validation_data=(dr.x_test, dr.y_test),
                    callbacks=[early_stop, early_stop2])

res = model.evaluate(dr.x_test, dr.y_test, verbose=0)
print("acc is: ", res[1] * 100)

model.save('./trained_models/0529_30_epochs.h5')