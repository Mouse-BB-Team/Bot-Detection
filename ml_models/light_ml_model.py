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

        predicted_class_name = imagenet_labels[predicted_class]

        print(predicted_class_name)

        data_root = tf.keras.utils.get_file(
            'flower_photos', 'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
            untar=True)

        image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
        image_data = image_generator.flow_from_directory(str(data_root), target_size=LightMlModel.IMAGE_SHAPE)

        for image_batch, label_batch in image_data:
            break

        result_batch = classifier.predict(image_batch)

        predicted_class_names = imagenet_labels[np.argmax(result_batch, axis=-1)]

        feature_extractor_layer = hub.KerasLayer(LightMlModel.feature_extractor_url,
                                                 input_shape=(224, 224, 3))

        feature_batch = feature_extractor_layer(image_batch)
        feature_extractor_layer.trainable = False

        model = tf.keras.Sequential([
            feature_extractor_layer,
            layers.Dense(image_data.num_classes)
        ])

        predictions = model(image_batch)

        model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['acc'])

        steps_per_epoch = np.ceil(image_data.samples / image_data.batch_size)

        batch_stats_callback = CollectBatchStats()

        history = model.fit(image_data, epochs=2,
                            steps_per_epoch=steps_per_epoch,
                            callbacks=[batch_stats_callback])

        class_names = sorted(image_data.class_indices.items(), key=lambda pair: pair[1])
        class_names = np.array([key.title() for key, value in class_names])
        print(class_names)

        predicted_batch = model.predict(image_batch)
        predicted_id = np.argmax(predicted_batch, axis=-1)
        predicted_label_batch = class_names[predicted_id]

        label_id = np.argmax(label_batch, axis=-1)

        prediction_result = ["correct" if predicted_id[n] == label_id[n] else "wrong" for n in range(30)]

        print(prediction_result)

        return history.history["acc"]
