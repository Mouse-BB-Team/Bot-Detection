import tensorflow as tf
import tensorflow_hub as hub


class InceptionV3:

    def __init__(self, training: (list, list), validation: (list, list)):
        self.training = training
        self.validation = validation

    def run(self):

        model = tf.keras.Sequential([
            hub.KerasLayer("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/4",
                           trainable=False),
            tf.keras.layers.Dense(30, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.build([None, 299, 299, 3])

        model.summary()

        initial_learning_rate = 0.0001
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate,
            decay_steps=100000,
            decay_rate=0.96,
            staircase=True)

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
                      loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        history = model.fit(self.training, epochs=1, batch_size=128,
                            validation_data=self.validation)

        return history.history
