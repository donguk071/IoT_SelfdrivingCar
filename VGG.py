import tensorflow as tf
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.optimizers import Adam
import read_data

dr = read_data.DataReader()
dr.f_data_reader(200)


# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), input_shape = (200,200,3),activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2000, activation=tf.nn.relu),
    tf.keras.layers.Dense(8, activation=tf.nn.softmax)
])

# Compile the model
model.compile(optimizer=Adam(lr=0.001), metrics=['accuracy'], loss='sparse_categorical_crossentropy')

print("model defined\n\n", model.summary())

print("\n\n************ TRAINING START ************")
early_stop = EarlyStopping(monitor='val_loss', patience=3)
early_stop2 = EarlyStopping(monitor='val_accuracy', patience=3)
print(dr.y_train.dtype)
history = model.fit(dr.x_train, dr.y_train, epochs=15, batch_size=32,
                    validation_data=(dr.x_test, dr.y_test),
                    callbacks=[early_stop, early_stop2])

res = model.evaluate(dr.x_test, dr.y_test, verbose=0)
print("acc is: ", res[1] * 100)

model.save('./trained_models/model1_20_epochs.h5')
