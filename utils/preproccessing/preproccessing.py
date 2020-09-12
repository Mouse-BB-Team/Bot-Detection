from math import floor
from random import shuffle
from pandas import DataFrame
import numpy as np
from matplotlib import pyplot
import tensorflow as tf

BOT_USER = 'usr-71'
TRAINING_SET_PERCENT = 0.25
SCALE_X = 299
SCALE_Y = 299


def __count_elements(dataset_list: list):
    total = 0
    for element in dataset_list:
        total += len(element)  # TODO len from sequenceLength
    return total


def __get_datasets(dataset: list, size: int):
    total = 0
    training_set = []
    validation_set = []
    for element in dataset:
        if total < size:
            training_set.append(element)
            total += len(element)
        else:
            validation_set.append(element)
    return training_set, validation_set


def __map_dataset(dataset: dict):
    result_dataset = []
    for key in dataset.keys():
        result_dataset.extend(dataset[key])
    return result_dataset


def get_datasets(dataset):
    bot_dataset = dataset[BOT_USER]
    del dataset[BOT_USER]

    user_dataset = __map_dataset(dataset)

    total_user_elements = __count_elements(user_dataset)
    total_bot_elements = __count_elements(bot_dataset)
    training_user_set_size = floor(TRAINING_SET_PERCENT * total_user_elements)
    training_bot_set_size = floor(TRAINING_SET_PERCENT * total_bot_elements)

    training_user_set, validation_user_set = __get_datasets(user_dataset, training_user_set_size)
    training_bot_set, validation_bot_set = __get_datasets(bot_dataset, training_bot_set_size)

    # training_bot_set = training_bot_set * 10
    # validation_bot_set = validation_bot_set * 10

    training_set = training_user_set + training_bot_set
    validation_set = validation_user_set + validation_bot_set
    training_labels = [0 for _ in range(len(training_user_set))] + [1 for _ in range(len(training_bot_set))]
    validation_labels = [0 for _ in range(len(validation_user_set))] + [1 for _ in range(len(validation_bot_set))]

    training_tuple = [(element, label) for element, label in zip(training_set, training_labels)]
    validation_tuple = [(element, label) for element, label in zip(validation_set, validation_labels)]

    shuffle(training_tuple)
    shuffle(validation_tuple)

    training_set = [element[0] for element in training_tuple]
    validation_set = [element[0] for element in validation_tuple]
    training_labels = [element[1] for element in training_tuple]
    validation_labels = [element[1] for element in validation_tuple]
    training_labels = np.array(training_labels)
    validation_labels = np.array(validation_labels)

    training_set = __paint_pictures(training_set)
    validation_set = __paint_pictures(validation_set)

    return (training_set, training_labels), (validation_set, validation_labels)


def __scale_and_print(sequence: DataFrame, x_res: int, y_res: int):
    x_resolution = sequence['events'][0]['xResolution']
    y_resolution = sequence['events'][0]['yResolution']

    scaler_x = x_res / x_resolution
    scaler_y = y_res / y_resolution

    array = np.zeros((x_res, y_res, 3), dtype=float)

    prev_x = __getX(sequence['events'][0])
    prev_y = __getY(sequence['events'][0])

    for element in sequence['events'][1:]:
        x = __getX(element)
        y = __getY(element)

        points = __interpolate_points((prev_x, prev_y), (x, y))

        x_points = [floor(p[0] * scaler_x) for p in points]
        y_points = [floor(p[1] * scaler_y) for p in points]

        __add_points_to_array(x_points, y_points, array)

        prev_x = x
        prev_y = y

    # __print_picture(array[:, :, 0], x_res, y_res)

    return array


def __add_points_to_array(x_points, y_points, array):
    for e in zip(x_points, y_points):
        array[e[0]][e[1]][0] = 1.0


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


def __getX(element: dict):
    if 'xCoordinate' in element:
        return element['xCoordinate']
    else:
        return 0


def __getY(element: dict):
    if 'yCoordinate' in element:
        return element['yCoordinate']
    else:
        return 0


def __print_picture(array, x_res, y_res):
    pyplot.imshow(array, interpolation='none')
    # pyplot.xticks(np.arange(0, x_res, 1))
    # pyplot.yticks(np.arange(0, y_res, 1))
    pyplot.show()


def __paint_pictures(dataset: list):
    result_dataset = []

    for element in dataset:
        result_dataset.append(__scale_and_print(element, SCALE_X, SCALE_Y))

    return np.array(result_dataset)

