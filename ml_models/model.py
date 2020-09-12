import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt


class ConvolutionalNetwork:

    def __init__(self, training: (list, list), validation: (list, list)):
        self.training = training
        self.validation = validation

    def run(self):
        train_images = self.training[0]
        train_labels = self.training[1]
        test_images = self.validation[0]
        test_labels = self.validation[1]

        model = tf.keras.Sequential([
            hub.KerasLayer("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/4",
                           trainable=True),  # Can be True, see below.
            tf.keras.layers.Dense(2, activation='softmax')
        ])
        model.build([None, 299, 299, 3])  # Batch input shape.

        model.summary()

        model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.000001),
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        history = model.fit(train_images, train_labels, epochs=1,
                            validation_data=(test_images, test_labels))

        # test_loss, test_acc = model.evaluate(test_images, test_labels)

        return history.history

        # print(test_acc)

        # plt.plot(history.history['accuracy'], label='accuracy')
        # plt.plot(history.history['val_accuracy'], label='val_accuracy')
        # plt.plot(history.history['loss'], label='loss')
        # plt.plot(history.history['val_loss'], label='val_loss')
        # plt.xlabel('Epoch')
        # plt.ylabel('Accuracy')
        # plt.ylim([0.5, 1])
        # plt.legend(loc='lower right')
        # plt.show()