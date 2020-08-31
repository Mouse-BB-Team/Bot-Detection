import re

class ConvolutionalNetwork:
    def run(self, card):
        import tensorflow as tf
        from tensorflow.keras import datasets, layers, models

        devices = tf.config.experimental.get_visible_devices('GPU')
        # tf.config.experimental.set_memory_growth(card, True)
        tf.config.experimental.set_virtual_device_configuration(
            devices[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
        tf.config.experimental.set_virtual_device_configuration(
            devices[1],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])

        logical_gpus = tf.config.experimental.list_logical_devices('GPU')[0]

        with tf.device(logical_gpus.name):
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

            model.summary()

            model.add(layers.Flatten())
            model.add(layers.Dense(64, activation='relu'))
            model.add(layers.Dense(10))

            model.summary()

            model.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

            history_model_result = model.fit(train_images, train_labels, epochs=1, verbose=2,
                                             validation_data=(test_images, test_labels))

        return history_model_result.history
