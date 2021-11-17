# ETL-Pipeline-Brazilian-E-Commerce-Data
## About Project
Data pipeline of Brazilian E-Commerce data

This repo provides scripts to download and preprocess data for Brazilian E-Commerce data. The raw data comes from [here](https://www.kaggle.com/olistbr/brazilian-ecommerce) of **Brazilian E-Commerce** You can find data in [brazilian-e-commerce s3 bucket](https://s3.console.aws.amazon.com/s3/home?region=eu-central-1#)

### Built With
-  Python
-  Spark
-  Airflow

## Getting Started
### Prerequisites
-  python 3.7.x
-  Download Docker if does not exist for see the pipeline
### Instructions
1. **Execute ```docker build -t etl-pipeline .``` command in the directory where the docker file is located**
2. **Execute ```docker run -p 8080:8080 etl-pipeline``` command**

+ This command build and docker image that containd Airflow. You will access the Airflow user interface from ```http://localhost:8080/``` after all requirements are installed. This is what the pipeline looks like.
![alt text](https://github.com/deniztas/ETL-Pipeline-Brazilian-E-Commerce-Data/blob/main/dag/pipeline_image.PNG)
3. **Switch from off to on the DAG, click the `brazilian-e-commerce-etl` and Trigger DAG**
- Output folders in the brazilian-e-commerce s3 bucket output folder
### Pipeline Definition
-   Each parallel task executes the `data_pipeline/module_runner.py`. This class derived from `etl_base.py`
-   csv url, output parquet and input parquet paths are retrieved with the help of config.py. `run_etl` function in the base is executed from sub classes. And pipeline starts.
-   Read and write functions are in `helper/read_write.py`. This functions takes table schema optionally. Table shema is kept in schema.yaml.
-   After csv is read, data_cleaning function runs sequentially.
-   `data_cleaning` function get not null rows according to not_null_columns information. This info is kept in schema.yaml as list.
-   After data cleaning each data frame is written their output path as parquet format.
-   Finally the `missed_order` task that trigger the `missed_order.py` runs. This script find which sellers missed their orders’ deadline to be
delivered to a carrier.
-   This pipeline runs on Airflow. The dag is in `/dag/etl_pipeline.py` path. BashOperators that trigger the `module_runner.py` script is created dynamically.
