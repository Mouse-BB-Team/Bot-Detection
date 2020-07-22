from utils.deserializer.protobuf_deserializer import ProtoLoader
from pathlib import Path
import pandas as pd
import pytest

PROTOFILES_DIR_PATH = Path(__file__).parent.joinpath("protofilesdir").absolute().__str__()


def test_should_return_single_df_sequence():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    filepath = Path(PROTOFILES_DIR_PATH).joinpath("test_file.pb").__str__()
    sequence = loader.get_single_sequence(filepath)
    assert isinstance(sequence, pd.DataFrame)


@pytest.mark.parametrize('arg', ["", ".txt", ".json", ".csv", ".xml"])
def test_should_raise_value_error_when_wrong_file_ext(arg):
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    filepath = Path(PROTOFILES_DIR_PATH).joinpath(f"test_file{arg}").__str__()
    with pytest.raises(ValueError):
        loader.get_single_sequence(filepath)


def test_should_return_correct_length_of_seq_list():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    seq_list = loader.get_list_of_sequences()
    assert len(seq_list) == 3


def test_should_return_list_of_sequences():
    loader = ProtoLoader(PROTOFILES_DIR_PATH)
    seq_list = loader.get_list_of_sequences()
    for seq in seq_list:
        assert isinstance(seq, pd.DataFrame)


def test_should_raise_file_not_found_error():
    loader = ProtoLoader(PROTOFILES_DIR_PATH + "/wrong/path")
    with pytest.raises(FileNotFoundError):
        loader.get_list_of_sequences()
