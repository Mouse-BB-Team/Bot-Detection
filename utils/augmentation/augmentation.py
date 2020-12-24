import argparse
from math import floor

import Augmentor
import os
import random
import shutil
from utils.deserializer.protobuf_deserializer import ProtoLoader
from utils.preproccessing.preprocessor import Preprocessor

USER_DIR = '/user'
BOT_DIR = '/bot'
TRAIN_DIR = '/train'
VAL_DIR = '/val'


def load_serialized_data(dataset_path):
    proto_loader = ProtoLoader(dataset_path)
    return proto_loader.get_list_of_sequences()


def save_data_to_images(user_dataset, path):
    preprocessor = Preprocessor(user_dataset)
    preprocessor.save_data_as_images(path, USER_DIR, BOT_DIR)


def augment_data(path, output_path, size):
    def _set_up_augmentor(input_path, output_dir):
        p = Augmentor.Pipeline(input_path, output_directory=output_dir)
        p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
        p.zoom(probability=0.3, min_factor=1.1, max_factor=1.6)
        p.flip_top_bottom(0.3)
        p.flip_left_right(0.3)
        return p

    _set_up_augmentor(path + USER_DIR, output_path + USER_DIR).sample(size)
    _set_up_augmentor(path + BOT_DIR, output_path + BOT_DIR).sample(size)


def create_tmp_dir(temp_dir):
    os.mkdir(temp_dir)
    os.mkdir(temp_dir + USER_DIR)
    os.mkdir(temp_dir + BOT_DIR)


def delete_tmp_dir(temp_dir):
    shutil.rmtree(temp_dir)


def create_dir_if_not_exists(dir):
    if not os.path.isdir(dir):
        create_tmp_dir(dir)
    else:
        delete_tmp_dir(dir)
        create_tmp_dir(dir)


def get_file_names(dir):
    listed_dir = [os.path.join(dir, file) for file in os.listdir(dir)]
    return [file for file in listed_dir if os.path.isfile(file)]


def move_files(filenames, dest):
    for file in filenames:
        shutil.move(file, dest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Augment data')
    parser.add_argument('-d', required=True, type=str, help='directory to dataset')
    parser.add_argument('-o', required=True, type=str, help='directory to output images')
    parser.add_argument('-s', required=False, type=int, help='number of samples in each dataset part (default=30000)', default=30000)
    parser.add_argument('--val_split', required=False, type=int, help='percentage value of dataset split for validation (default=20%)', default=20)
    args = parser.parse_args()
    dataset_path = args.d
    output_path = args.o
    size = args.s
    split = args.val_split

    rand_value = str(random.randint(100000, 1000000))
    temp_dir = '/tmp/bot_detection_data_' + rand_value
    temp_aug_dir = '/tmp/bot_detection_augmentation_' + rand_value

    create_dir_if_not_exists(temp_dir)
    create_dir_if_not_exists(temp_aug_dir)

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    create_dir_if_not_exists(output_path + TRAIN_DIR)
    create_dir_if_not_exists(output_path + VAL_DIR)

    dataset = load_serialized_data(dataset_path)
    save_data_to_images(dataset, temp_dir)
    augment_data(temp_dir, temp_aug_dir, size)

    val_samples = floor(size * (split / 100))
    train_samples = size - val_samples

    user_data_files = get_file_names(temp_aug_dir + USER_DIR)
    bot_data_files = get_file_names(temp_aug_dir + BOT_DIR)

    random.shuffle(user_data_files)
    random.shuffle(bot_data_files)

    train_user_files = user_data_files[0:train_samples]
    train_bot_samples = bot_data_files[0:train_samples]

    val_user_files = user_data_files[train_samples:]
    val_bot_files = bot_data_files[train_samples:]

    move_files(train_user_files, output_path + TRAIN_DIR + USER_DIR)
    move_files(train_bot_samples, output_path + TRAIN_DIR + BOT_DIR)
    move_files(val_user_files, output_path + VAL_DIR + USER_DIR)
    move_files(val_bot_files, output_path + VAL_DIR + BOT_DIR)

    delete_tmp_dir(temp_dir)
    delete_tmp_dir(temp_aug_dir)

