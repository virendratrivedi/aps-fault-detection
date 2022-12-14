import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
import yaml


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:

    """
    Description: This function return collection as dataframe 
    ===========================================
    params:
    database_name: database_name
    collection_name: collection_name
    ===========================================
    return Pandas dataframe
    """
    try:
        logging.info("Reading data from database {database_name} and Collecion {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found Column: {df.columns}")
        if '_id' in df.columns:
            logging.info(f"Dropping Column: _id")
            df=df.drop("_id",axis=1)
        logging.info(f"Rows and column in df: {df.shape}")    
        return df    

    except Exception as e:
        raise SensorException(e, sys)    

    
def write_ymal_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)

        with open(file_path,"w") as file_writer:
            yaml.dump(data, file_writer)
              

    except Exception as e:
        raise SensorException(e, sys)  


def convert_column_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:

        for column in df.columns:
            if column not in exclude_columns:
                df[column] = df[column].astype('float')

        return df 
    except Exception as e:
        raise SensorException(e, sys)           

        



