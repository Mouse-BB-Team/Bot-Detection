import argparse
import Augmentor
import os
import random
import shutil
from utils.deserializer.protobuf_deserializer import ProtoLoader
from utils.preproccessing.preprocessor import Preprocessor

USER_DIR = '/user'
BOT_DIR = '/bot'


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Augment data')
    parser.add_argument('-d', required=True, type=str, help='directory to dataset')
    parser.add_argument('-o', required=True, type=str, help='directory to output images')
    parser.add_argument('-s', required=False, type=int, help='number of samples in each dataset part', default=30000)
    args = parser.parse_args()
    dataset_path = args.d
    output_path = args.o
    size = args.s

    temp_dir = '/tmp/bot_detection_augmentation_' + str(random.randint(100000, 1000000))

    if not os.path.isdir(temp_dir):
        create_tmp_dir(temp_dir)
    else:
        delete_tmp_dir(temp_dir)
        create_tmp_dir(temp_dir)

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    dataset = load_serialized_data(dataset_path)
    save_data_to_images(dataset, temp_dir)
    augment_data(temp_dir, output_path, size)
    delete_tmp_dir(temp_dir)

