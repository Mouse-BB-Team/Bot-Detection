import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import numpy as np
import PIL.Image as Image


class CollectBatchStats(tf.keras.callbacks.Callback):
    def __init__(self):
        self.batch_losses = []
        self.batch_acc = []

    def on_train_batch_end(self, batch, logs=None):
        self.batch_losses.append(logs['loss'])
        self.batch_acc.append(logs['acc'])
        self.model.reset_metrics()


class LightMlModel:
    classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"
    feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2"
    IMAGE_SHAPE = (224, 224)

    def __init__(self):
        pass

    def run(self):
        grace_hopper = tf.keras.utils.get_file('image.jpg',
                                               'https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg')
        classifier = tf.keras.Sequential([
            hub.KerasLayer(LightMlModel.classifier_url, input_shape=LightMlModel.IMAGE_SHAPE + (3,))
        ])
        grace_hopper = Image.open(grace_hopper).resize(LightMlModel.IMAGE_SHAPE)

        grace_hopper = np.array(grace_hopper) / 255.0

        result = classifier.predict(grace_hopper[np.newaxis, ...])

        predicted_class = np.argmax(result[0], axis=-1)

        labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                              'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
        imagenet_labels = np.array(open(labels_path).read().splitlines())

        data_root = tf.keras.utils.get_file(
            'flower_photos', 'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
            untar=True)

        image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
        image_data = image_generator.flow_from_directory(str(data_root), target_size=LightMlModel.IMAGE_SHAPE)

        feature_extractor_layer = hub.KerasLayer(LightMlModel.feature_extractor_url, input_shape=(224, 224, 3))

        feature_extractor_layer.trainable = False

        model = tf.keras.Sequential([
            feature_extractor_layer,
            layers.Dense(image_data.num_classes),
            layers.Dense(1, activation='sigmoid')
        ])

        base_learning_rate = 0.0001
        model.compile(loss=tf.losses.BinaryCrossentropy(from_logits=True),
                      optimizer=tf.optimizers.RMSprop(lr=base_learning_rate / 10),
                      metrics=[
                          tf.metrics.BinaryAccuracy(name='accuracy'),
                          tf.metrics.FalsePositives(name='false_positives'),
                          tf.metrics.TrueNegatives(name='true_negatives'),
                          tf.metrics.FalseNegatives(name='false_negatives'),
                          tf.metrics.TruePositives(name='true_positives')
                      ])

        steps_per_epoch = np.ceil(image_data.samples / image_data.batch_size)

        batch_stats_callback = CollectBatchStats()

        history = model.fit(image_data, epochs=2,
                            steps_per_epoch=steps_per_epoch,
                            callbacks=[batch_stats_callback])

        return history.history
