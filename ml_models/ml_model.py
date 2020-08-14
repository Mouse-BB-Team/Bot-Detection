import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds


# tfds.disable_progress_bar()


class MlModelExample:
    IMG_SIZE = 130
    BATCH_SIZE = 32
    SHUFFLE_BUFFER_SIZE = 1000
    IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

    def __init__(self):
        self.data = self.__load_example_data()
        self.pretrained_model = tf.keras.applications.MobileNetV2(input_shape=self.IMG_SHAPE,
                                                                  include_top=False,
                                                                  weights='imagenet')
        self.train_data = self.data[0]
        self.validation_data = self.data[1]
        self.test_data = self.data[0]

    def run(self):
        train = self.train_data.map(self.__format_example)
        validation = self.validation_data.map(self.__format_example)
        test = self.test_data.map(self.__format_example)

        train_batches = train.shuffle(self.SHUFFLE_BUFFER_SIZE).batch(self.BATCH_SIZE)
        validation_batches = validation.batch(self.BATCH_SIZE)
        test_batches = test.batch(self.BATCH_SIZE)

        for image_batch, label_batch in train_batches.take(1):
            pass


        # Create the base model from the pre-trained model MobileNet V2
        base_model = self.pretrained_model
        feature_batch = base_model(image_batch)

        # Here we will extract features from pretrained model,
        # then put them into our classifier
        base_model.trainable = False
        # base_model.summary()

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        feature_batch_average = global_average_layer(feature_batch)

        prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')
        prediction_batch = prediction_layer(feature_batch_average)

        model = tf.keras.Sequential([
            base_model,
            global_average_layer,
            prediction_layer
        ])

        base_learning_rate = 0.0001
        model.compile(optimizer=tf.optimizers.RMSprop(lr=base_learning_rate),
                      loss=tf.losses.BinaryCrossentropy(from_logits=True),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        initial_epochs = 1
        validation_steps = 5

        loss0, accuracy0, fp0, tn0, fn0, tp0 = model.evaluate(validation_batches, steps=validation_steps)

        print("initial loss: {:.2f}".format(loss0))
        print("initial accuracy: {:.2f}".format(accuracy0))
        print(f"initial FP: {fp0}")
        print(f"initial TN: {tn0}")
        print(f"initial FN: {fn0}")
        print(f"initial TP: {tp0}")

        history = model.fit(train_batches,
                            epochs=initial_epochs,
                            validation_data=validation_batches)

        base_model.trainable = True
        # Let's take a look to see how many layers are in the base model
        print("Number of layers in the base model: ", len(base_model.layers))

        # Fine-tune from this layer onwards
        fine_tune_at = 100

        # Freeze all the layers before the `fine_tune_at` layer
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

        # metrics available https://keras.io/api/metrics
        model.compile(loss=tf.losses.BinaryCrossentropy(from_logits=True),
                      optimizer=tf.optimizers.RMSprop(lr=base_learning_rate / 10),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        fine_tune_epochs = 1
        total_epochs = initial_epochs + fine_tune_epochs

        history_fine = model.fit(train_batches,
                                 epochs=total_epochs,
                                 initial_epoch=history.epoch[-1],
                                 validation_data=validation_batches)

        return history_fine

    @staticmethod
    def __load_example_data():
        (raw_train, raw_validation, raw_test), _ = tfds.load(
            'cats_vs_dogs',
            split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
            with_info=True,
            as_supervised=True
        )
        return raw_train, raw_validation, raw_test

    def __format_example(self, image, label):
        image = tf.cast(image, tf.float32)
        image = (image / 127.5) - 1
        image = tf.image.resize(image, (self.IMG_SIZE, self.IMG_SIZE))
        return image, label
