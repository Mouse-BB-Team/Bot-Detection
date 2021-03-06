import os

from utils.deserializer.config.usersequence_pb2 import UserSequence
from read_protobuf import read_protobuf
from glob import glob
from pathlib import Path
import logging.config

logger_config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class ProtoLoader:
    def __init__(self, path_to_directory):
        self.path_to_directory = path_to_directory
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_single_sequence(self, filename):
        path_to_file = Path(self.path_to_directory).joinpath(filename).__str__()
        df_sequence = read_protobuf(path_to_file, UserSequence())
        return df_sequence

    def get_list_of_sequences(self):
        protofiles = self.__get_list_of_protofiles()
        df_sequences = {}
        if len(protofiles) == 0:
            self.logger.warning("No files found in directory \n%s ", self.path_to_directory)
            return list()
        for key in protofiles.keys():
            df_sequences[key] = [read_protobuf(pb, UserSequence()) for pb in protofiles[key]]
        return df_sequences

    def __get_list_of_protofiles(self):
        user_sequences = {}
        directories = os.listdir(self.path_to_directory)
        for directory in directories:
            search_path = Path(self.path_to_directory).joinpath(directory).joinpath("*").__str__()
            proto_files = [f for f in glob(search_path)]
            user_sequences[directory] = proto_files
        return user_sequences

