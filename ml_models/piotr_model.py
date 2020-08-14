import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt


class PiotrModel:
    def run(self):
        (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

        # Normalize pixel values to be between 0 and 1
        train_images, test_images = train_images / 255.0, test_images / 255.0
        class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                       'dog', 'frog', 'horse', 'ship', 'truck']

        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='sigmoid'))
        model.summary()

        base_learning_rate = 0.0001
        model.compile(optimizer=tf.optimizers.RMSprop(lr=base_learning_rate),
                      loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        history = model.fit(train_images, train_labels, epochs=10,
                            validation_data=(test_images, test_labels))
        loss0, accuracy0, fp0, tn0, fn0, tp0 = model.evaluate(test_images, test_labels, verbose=2)

        print(loss0, accuracy0, fp0, tn0, fn0, tp0)

        return history
