from etl_base import EtlBase
import argparse


class OlistCustomer(EtlBase):

    def __init__(self, table_name: str):
        super().__init__(table_name)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', type=str, required=True)
    args = parser.parse_args()
    instance = OlistCustomer(table_name=args.table_name)
    instance.run_etl()
