import logging

from pyspark.sql.utils import AnalysisException
from pyspark.sql import DataFrame, functions as F

from config import get_config, get_table_schema
from helper.read_write import read_data, write_data


class EtlBase():
    def __init__(self, table_name: str):
        pipeline_config = get_config()
        self.raw_data_path = pipeline_config.get("tables").get(table_name).get("raw_data_path")
        self.output_path = pipeline_config.get("tables").get(table_name).get("output_path")
        schema_file_name = pipeline_config.get("schema_file")
        self.table_schema = get_table_schema(
            schema_file=schema_file_name, table_name=table_name).get("schema")
        self.not_null_columns = self.table_schema = get_table_schema(
            schema_file=schema_file_name, table_name=table_name).get("not_null_columns")
        self.output_data = None

    def read(self, csv_delimiter: str = ","):
        try:
            self.output_data = read_data(
                raw_data_path=self.raw_data_path,
                header=True,
                sep=csv_delimiter
            )
        except AnalysisException as ex:
            logging.critical(f"Csv file not found in path: {self.raw_data_path}.")
            raise ex

        logging.warn("read_data completed")

    def data_cleaning(self):
        for column in self.not_null_columns:
            self.output_data = self.output_data.where(F.col(column).isNotNull())

    def write(self, data: DataFrame, output_path: str, file_type: str):
        """Saves data to output directory."""
        write_data(
            df=data,
            output_path=output_path,
            file_type=file_type,
            partition_number=1,
            schema=self.table_schema)
    
    def run_etl(self):
        self.read()
        self.data_cleaning()
        self.write(data=self.output_data, output_path=self.output_path, file_type="parquet")
