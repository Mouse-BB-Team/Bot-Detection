from avro.datafile import DataFileReader
from avro.io import DatumReader
from pathlib import Path
import pandavro as pdx
import json


class AvroLoader:
    DEFAULT_SCHEMA_PATH = Path(__file__).parent.parent.parent.absolute().joinpath('config/avro_schema.json')

    def __init__(self, schema_config_path=DEFAULT_SCHEMA_PATH):
        self.schema_config_path = schema_config_path

    def __load_schema(self):
        with open(self.schema_config_path) as f:
            json_schema = json.load(f)
        return json_schema

    def read_avro_to_pandas_df(self, avro_file_path, sort=True, sort_by='sequenceId'):
        df = pdx.read_avro(avro_file_path, self.__load_schema())
        return df.sort_values(sort_by) if sort else df

    @staticmethod
    def get_avro_reader(avro_file_path):
        return DataFileReader(open(avro_file_path, "rb"), DatumReader())
