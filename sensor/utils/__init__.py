import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys

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
        raise SensorException(e, s)    

    