from typing import List
from pandas import DataFrame
from utils.deserializer.config.usersequence_pb2 import UserSequence
from read_protobuf import read_protobuf
from glob import glob
from pathlib import Path


class ProtoLoader:
    def __init__(self, path_to_directory):
        self.path_to_directory = path_to_directory

    def get_single_sequence(self, filename):
        if filename.endswith(".pb"):
            path_to_file = Path(self.path_to_directory).joinpath(filename).__str__()
        else:
            raise ValueError("Wrong file extension! Should be '*.pb'")

        df_sequence = read_protobuf(path_to_file, UserSequence())
        return df_sequence

    def get_list_of_sequences(self) -> List[DataFrame]:
        protofiles = self.__get_list_of_protofiles()
        if len(protofiles) == 0:
            raise FileNotFoundError("No protobuf files found in given directory")

        df_sequences = [read_protobuf(pb, UserSequence()) for pb in protofiles]
        return df_sequences

    def __get_list_of_protofiles(self):
        search_path = Path(self.path_to_directory).joinpath("*.pb").__str__()
        proto_files = [f for f in glob(search_path)]
        return proto_files
