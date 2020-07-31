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

        # print(image_batch.shape)

        # Create the base model from the pre-trained model MobileNet V2
        base_model = self.pretrained_model
        feature_batch = base_model(image_batch)
        # print(feature_batch.shape)

        # Here we will extract features from pretrained model,
        # then put them into our classifier
        base_model.trainable = False
        # base_model.summary()

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        feature_batch_average = global_average_layer(feature_batch)
        # print(feature_batch_average.shape)

        prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')
        prediction_batch = prediction_layer(feature_batch_average)
        # print(prediction_batch.shape)

        model = tf.keras.Sequential([
            base_model,
            global_average_layer,
            prediction_layer
        ])

        base_learning_rate = 0.0001
        model.compile(optimizer=tf.optimizers.RMSprop(lr=base_learning_rate),
                      loss=tf.losses.BinaryCrossentropy(from_logits=True),
                      # metrics available: https://keras.io/api/metrics
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='FP'),
                          tf.metrics.TrueNegatives(name='TN'),
                          tf.metrics.FalseNegatives(name='FN'),
                          tf.metrics.TruePositives(name='TP')
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

        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']

        loss = history.history['loss']
        val_loss = history.history['val_loss']

        far = [fp / (fp + tn) for fp, tn in zip(history.history['FP'], history.history['TN'])]
        far_loss = [fp / (fp + tn) for fp, tn in zip(history.history['val_FP'], history.history['val_TN'])]

        frr = [fn / (fn + tp) for fn, tp in zip(history.history['FN'], history.history['TP'])]
        frr_loss = [fn / (fn + tp) for fn, tp in zip(history.history['val_FN'], history.history['val_TP'])]

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
                          tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy'),
                          tf.metrics.FalsePositives(name='FP'),
                          tf.metrics.TrueNegatives(name='TN'),
                          tf.metrics.FalseNegatives(name='FN'),
                          tf.metrics.TruePositives(name='TP')
                      ])

        fine_tune_epochs = 1
        total_epochs = initial_epochs + fine_tune_epochs

        history_fine = model.fit(train_batches,
                                 epochs=total_epochs,
                                 initial_epoch=history.epoch[-1],
                                 validation_data=validation_batches)

        acc += history_fine.history['accuracy']
        val_acc += history_fine.history['val_accuracy']

        far += [fp / (fp + tn) for fp, tn in zip(history_fine.history['FP'], history_fine.history['TN'])]
        far_loss += [fp / (fp + tn) for fp, tn in zip(history_fine.history['val_FP'], history_fine.history['val_TN'])]

        frr += [fn / (fn + tp) for fn, tp in zip(history_fine.history['FN'], history_fine.history['TP'])]
        frr_loss += [fn / (fn + tp) for fn, tp in zip(history_fine.history['val_FN'], history_fine.history['val_TP'])]

        loss += history_fine.history['loss']
        val_loss += history_fine.history['val_loss']

        return (acc, val_acc), (loss, val_loss), (far, far_loss), (frr, frr_loss)

    def __load_example_data(self):
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
