import utils.pyloader.loader
from pathlib import Path
import pandas as pd
import avro

SCHEMA_PATH = Path(__file__).parent.parent.parent.parent.absolute().joinpath('config/avro_schema.json')
TEST_FILE_PATH = "test/test_avro.avro"


def test_should_return_df_from_avro_file():
    avro_loader = utils.pyloader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df(TEST_FILE_PATH)
    assert isinstance(df, pd.DataFrame)


def test_should_return_sorted_df():
    avro_loader = utils.pyloader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df(TEST_FILE_PATH, sort=True)
    assert df['sequenceId'].is_monotonic_increasing


def test_should_return_not_sorted_df():
    avro_loader = utils.pyloader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df(TEST_FILE_PATH, sort=False)
    assert not df['sequenceId'].is_monotonic_increasing


def test_should_validate_reader_is_not_none():
    reader = utils.pyloader.loader.AvroLoader.get_avro_reader(TEST_FILE_PATH)
    assert reader is not None


def test_should_return_avro_reader():
    reader = utils.pyloader.loader.AvroLoader.get_avro_reader(TEST_FILE_PATH)
    assert isinstance(reader, avro.datafile.DataFileReader)
