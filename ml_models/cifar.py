import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import datasets, layers, models


class Cifar:

    def __init__(self, training: (list, list), validation: (list, list)):
        self.training = training
        self.validation = validation

    def run(self):
        train_images = self.training[0]
        train_labels = self.training[1]
        test_images = self.validation[0]
        test_labels = self.validation[1]

        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(2))

        model.summary()

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        history = model.fit(train_images, train_labels, epochs=10,
                            validation_data=(test_images, test_labels))

        test_loss, test_acc = model.evaluate(test_images, test_labels)

        print(test_acc)