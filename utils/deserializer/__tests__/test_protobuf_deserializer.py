from utils.deserializer.protobuf_deserializer import ProtoLoader
from pathlib import Path
import pandas as pd
import pytest

PROTOFILES_DIR_PATH = Path(__file__).parent.joinpath("protofilesdir").absolute().__str__()
INVALID_PATH = "some/wrong/path"


@pytest.mark.parametrize('filepath', ["test_file.pb", "test_file_1.txt", "test_file_2.xml"])
def test_should_return_single_df_sequence(filepath):
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    sequence = loader.get_single_sequence(filepath)
    assert isinstance(sequence, pd.DataFrame)


def test_should_return_not_none_when_directory_not_empty():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    seq_list = loader.get_list_of_sequences()
    assert seq_list is not None


def test_should_return_correct_length_of_seq_list():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    seq_list = loader.get_list_of_sequences()
    assert len(seq_list) == 3


def test_should_return_empty_list_when_directory_empty():
    loader = ProtoLoader(PROTOFILES_DIR_PATH + INVALID_PATH)
    seq_list = loader.get_list_of_sequences()
    assert len(seq_list) == 0


def test_should_check_for_list_when_directory_empty():
    loader = ProtoLoader(PROTOFILES_DIR_PATH + INVALID_PATH)
    seq_list = loader.get_list_of_sequences()
    assert isinstance(seq_list, list)


def test_should_return_list_of_sequences():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    seq_list = loader.get_list_of_sequences()
    for seq in seq_list:
        assert isinstance(seq, pd.DataFrame)
