from tensorflow import keras
from tensorflow.keras.optimizers import Adam 
import read_data


dr = read_data.DataReader()
dr.f_data_reader(200)

# model = keras.Sequential([
#     # 이걸 수정해보자
#     keras.layers.Conv2D(filters=64, kernel_size=(3,3), input_shape = (200,200,3), activation ='ReLU' ),
    
#     keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.MaxPooling2D((2,2)),
#     keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.MaxPooling2D((2,2)),
#     keras.layers.Conv2D(filters=256, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.Conv2D(filters=256, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.MaxPooling2D((2,2)),
#     keras.layers.Conv2D(filters=512, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.Conv2D(filters=512, kernel_size=(3,3), activation ='ReLU' ),
#     keras.layers.MaxPooling2D((2,2)),
#     keras.layers.Flatten(),
#     keras.layers.Dense(4096, activation = 'ReLU'),
#     keras.layers.Dense(4096, activation = 'ReLU'),
#     keras.layers.Dense(1000, activation = 'ReLU'),
#     #classifing 3
#     keras.layers.Dense(6, activation = 'softmax')
# ])
model = keras.Sequential([
    # 이걸 수정해보자
    keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation ='ReLU' ),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation ='ReLU' ),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation ='ReLU' ),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation ='ReLU' ),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation ='ReLU' ),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(2000, activation = 'ReLU'),
    keras.layers.Dense(6, activation = 'softmax')
])

model.compile(optimizer = Adam(learning_rate= 0.001), metrics=['accuracy'],loss = 'sparse_categorical_crossentropy')
print("model definded\n\n", model.summary)

print("\n\n************ TRAINING START ************ ")
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
early_stop2 = keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=3)
print(dr.y_train.dtype)
history = model.fit(dr.x_train, dr.y_train, epochs=20, batch_size= 32,
                    validation_data=(dr.x_test, dr.y_test),
                    callbacks=[early_stop, early_stop2])

res = model.evaluate(dr.x_test,dr.y_test,verbose = 0 )
print("acc is : ", res[1]* 100)

model.save('./models/model1_20_epochs.h5')
