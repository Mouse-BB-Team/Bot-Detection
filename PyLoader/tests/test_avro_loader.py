import PyLoader.loader
from pathlib import Path
import pandas as pd
import avro

SCHEMA_PATH = Path(__file__).parent.parent.parent.absolute().joinpath('config/avro_schema.json')


def test_should_return_df_from_avro_file():
    avro_loader = PyLoader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df("test/test_avro.avro")
    assert isinstance(df, pd.DataFrame)


def test_should_return_sorted_df():
    avro_loader = PyLoader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df("test/test_avro.avro", sort=True, sort_by='sequenceId')
    assert df['sequenceId'].is_monotonic_increasing


def test_should_return_not_sorted_df():
    avro_loader = PyLoader.loader.AvroLoader(SCHEMA_PATH)
    df = avro_loader.read_avro_to_pandas_df("test/test_avro.avro", sort=False)
    assert not df['sequenceId'].is_monotonic_increasing


def test_should_validate_reader_is_not_none():
    reader = PyLoader.loader.AvroLoader.get_avro_reader("test/test_avro.avro")
    assert reader is not None


def test_should_return_avro_reader():
    reader = PyLoader.loader.AvroLoader.get_avro_reader("test/test_avro.avro")
    assert isinstance(reader, avro.datafile.DataFileReader)
