import tensorflow as tf
import tensorflow_hub as hub


class InceptionV3:

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
                           trainable=False),
            tf.keras.layers.Dense(30, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.build([None, 299, 299, 3])

        model.summary()

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0000003),
                      loss=tf.keras.losses.BinaryCrossentropy(from_logits=True, label_smoothing=1),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        history = model.fit(train_images, train_labels, epochs=100,
                            validation_data=(test_images, test_labels))

        return history.history
