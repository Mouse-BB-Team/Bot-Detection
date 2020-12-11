from math import floor
from random import shuffle
from pandas import DataFrame
import numpy as np
from matplotlib import pyplot
from PIL import Image



BOT_USER = 'usr-71'
TRAIN_SET_PERCENT = 0.75
SCALE_X = 299
SCALE_Y = 299


class Preprocessor:

    def __init__(self, dataset, dims=(SCALE_X, SCALE_Y), train_set_percent=TRAIN_SET_PERCENT, bot_user_id=BOT_USER,
                 bot_dataset_multiplier=1, print_pictures=False):
        self.dataset = dataset
        self.dims = dims
        self.train_set_percent = train_set_percent
        self.bot_user_id = bot_user_id
        self.bot_set_multiplier = bot_dataset_multiplier
        self.print_pictures = print_pictures

    def get_datasets(self):
        user_set, bot_set = self.__extract_bot_dataset()

        training_user_set_size, training_bot_set_size = self.__count_dataset_sizes(user_set, bot_set)

        # training_user_set, validation_user_set = self.__split_sets(user_set, training_user_set_size)
        # training_bot_set, validation_bot_set = self.__split_sets(bot_set, training_bot_set_size)
        #
        # training_bot_set = self.__multiply_bot_set(training_bot_set)
        # validation_bot_set = self.__multiply_bot_set(validation_bot_set)
        #
        # training_dataset, training_labels = self.__make_dataset(training_user_set, training_bot_set)
        # validation_dataset, validation_labels = self.__make_dataset(validation_user_set, validation_bot_set)
        #
        # training_labels = np.array(training_labels)
        # validation_labels = np.array(validation_labels)

        # training_dataset = self.__generate_images(training_dataset)
        # validation_dataset = self.__generate_images(validation_dataset)

        user_set = self.__generate_images(user_set)
        bot_set = self.__generate_images(bot_set)

        self.print_picture(user_set[0])

        self._save_to_files(user_set, '/user')
        self._save_to_files(bot_set, '/bot')
        # return (training_dataset, training_labels), (validation_dataset, validation_labels)
        print()

    def _save_to_files(self, set, path):
        for i in range(0, len(set)):
            im = Image.fromarray(np.uint8(set[i]))
            # im.show()
            im.save('/home/piotr/Desktop/data/' + path + path + str(i) + '.jpg')

    def __extract_bot_dataset(self):
        bot_set = self.dataset[self.bot_user_id]
        del self.dataset[self.bot_user_id]

        user_set = self.__flat_dataset(self.dataset)
        return user_set, bot_set

    @staticmethod
    def __flat_dataset(dataset: dict):
        result_dataset = []
        for key in dataset.keys():
            result_dataset.extend(dataset[key])
        return result_dataset

    def __count_dataset_sizes(self, user_dataset, bot_dataset):
        total_user_elements = self.__count_elements(user_dataset)
        total_bot_elements = self.__count_elements(bot_dataset)
        training_user_set_size = floor(TRAIN_SET_PERCENT * total_user_elements)
        training_bot_set_size = floor(TRAIN_SET_PERCENT * total_bot_elements)
        return training_user_set_size, training_bot_set_size

    @staticmethod
    def __count_elements(dataset_list: list):
        total = 0
        for element in dataset_list:
            total += element['sequenceLength'][0]
        return total

    @staticmethod
    def __split_sets(dataset: list, split_size: int):
        total = 0
        training_set = []
        validation_set = []
        for element in dataset:
            if total < split_size:
                training_set.append(element)
                total += element['sequenceLength'][0]
            else:
                validation_set.append(element)
        return training_set, validation_set

    def __multiply_bot_set(self, bot_set):
        return bot_set * self.bot_set_multiplier

    def __make_dataset(self, user_set, bot_set):
        dataset = user_set + bot_set
        labels = self.__generate_labels(user_set, bot_set)
        return self.__shuffle_dataset(dataset, labels)

    @staticmethod
    def __generate_labels(user_set, bot_set):
        return [0 for _ in range(len(user_set))] + [1 for _ in range(len(bot_set))]

    @staticmethod
    def __shuffle_dataset(dataset, labels):
        dataset_tuple = [(element, label) for element, label in zip(dataset, labels)]
        shuffle(dataset_tuple)
        dataset = [element[0] for element in dataset_tuple]
        labels = [element[1] for element in dataset_tuple]
        return dataset, labels

    def __generate_images(self, dataset: list):
        result_dataset = []

        for element in dataset:
            result_dataset.append(self.__prepare_image(element, self.dims[0], self.dims[1]))

        return np.array(result_dataset)

    def __prepare_image(self, sequence: DataFrame, x_res: int, y_res: int):

        def get_x(e: dict):
            if 'xCoordinate' in e:
                return e['xCoordinate']
            else:
                return 0

        def get_y(e: dict):
            if 'yCoordinate' in e:
                return e['yCoordinate']
            else:
                return 0

        x_resolution = sequence['events'][0]['xResolution']
        y_resolution = sequence['events'][0]['yResolution']

        scaler_x = x_res / x_resolution
        scaler_y = y_res / y_resolution

        array = np.zeros((x_res, y_res, 3), dtype=int)

        prev_x = get_x(sequence['events'][0])
        prev_y = get_y(sequence['events'][0])

        for element in sequence['events'][1:]:
            x = get_x(element)
            y = get_y(element)

            points = self.__interpolate_points((prev_x, prev_y), (x, y))

            x_points = [floor(p[0] * scaler_x) for p in points]
            y_points = [floor(p[1] * scaler_y) for p in points]

            self.__add_points_to_array(x_points, y_points, array)

            prev_x = x
            prev_y = y


        # self.print_picture(array)
        return array

    @staticmethod
    def __interpolate_points(p1: (int, int), p2: (int, int)):
        points = [p1]

        if p1[0] == p2[0]:
            for i in range(p1[1] + 1, p2[1]):
                points.append((p1[0], i))
        else:
            a = (p2[1] - p1[1])/(p2[0] - p1[0])
            b = p1[1] - a * p1[0]

            for i in range(p1[0] + 1, p2[0]):
                points.append((i, floor(i * a + b)))

        points.append(p2)

        return points

    @staticmethod
    def __add_points_to_array(x_points, y_points, array):
        for e in zip(x_points, y_points):
            array[e[0]][e[1]][0] = 255

    @staticmethod
    def print_picture(array):
        pyplot.imshow(array, interpolation='none')
        pyplot.show()
