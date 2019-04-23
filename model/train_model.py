import os
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers. normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

data_set_name='set1'
classes = ['Accelerate', 'DoNothing', 'TurnLeft', 'TurnRight']

def get_data_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(script_dir,'..','data',data_set_name)
    return os.path.normpath(data_dir)


def get_model_dir():
    model_dir = os.path.join(get_data_dir(),'model')
    return os.path.normpath(model_dir)


def define_model(image_dim,num_channels,num_classes):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(image_dim, image_dim, num_channels)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Conv2D(96, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def read_train_dataframe():
    data_dir=get_data_dir()
    xls_path=os.path.join(data_dir,'data.xlsx')
    df = pd.read_excel(xls_path)
    return df


def get_data_generators(image_dim,batch_size):
    df=read_train_dataframe()
    data_generator = ImageDataGenerator(validation_split=0.2)
    train_generator = \
        data_generator.flow_from_dataframe(df,x_col='imgFile',y_col='action',
                                           target_size=(image_dim, image_dim),color_mode='grayscale',
                                           class_mode='categorical', batch_size=batch_size,
                                           classes=classes,
                                           subset='training')

    validation_generator = \
        data_generator.flow_from_dataframe(df,x_col='imgFile',y_col='action',
                                           target_size = (image_dim, image_dim),color_mode='grayscale',
                                           class_mode='categorical', batch_size=batch_size,
                                           classes=classes,
                                           subset="validation")

    return train_generator , validation_generator


df = read_train_dataframe();

print("Dataframe loaded")


num_channels = 1 #Grayscale images

image_dim = 256
batch_size = 32

train_generator , validation_generator = get_data_generators(image_dim,batch_size)

num_train_images=train_generator.samples
num_test_images=validation_generator.samples

print('Got generators')

num_classes = len(classes)

model = define_model(image_dim,num_channels,num_classes)

model.summary()

model_dir = get_model_dir()
os.makedirs(model_dir,exist_ok=True)
model_file = os.path.join(model_dir,'model_v3-{epoch:02d}-{val_acc:.2f}.h5')

checkpoint = ModelCheckpoint(model_file , monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit_generator(
        train_generator,
        steps_per_epoch=num_train_images/batch_size,
        epochs=50,
        validation_steps=num_test_images/batch_size,
        validation_data=validation_generator,
        callbacks=callbacks_list)


model.save(model_file)
