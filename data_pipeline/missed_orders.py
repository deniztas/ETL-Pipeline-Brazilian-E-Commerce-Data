from config import get_config
from helper.read_write import read_data, write_data

def missed_config():
    pipeline_config = get_config()
    order_items_path = pipeline_config.get("tables").get("olist_order_items").get("output_path")
    orders_path = pipeline_config.get("tables").get("olist_orders").get("output_path")
    output_path = pipeline_config.get("missed_orders_path")
    output = None
    order_items = read_data(
        raw_data_path=order_items_path,
        file_type = "parquet"
    )
    orders = read_data(
        raw_data_path=orders_path,
        file_type = "parquet"
    )
    
    output = order_items.join(orders, 
                              order_items.order_id == orders.order_id,
                              how="inner") \
                        .where(order_items.shipping_limit_date < orders.order_delivered_customer_date) \
                        .select(order_items.seller_id)
    write_data(
        df=output,
        output_path=output_path,
        file_type="parquet",
        partition_number=1)
    
if __name__ == "__main__":
    missed_config()
