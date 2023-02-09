import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
import yaml
import dill
import numpy as np


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

def save_object(file_path:str,obj:object)-> None:
    try:
        logging.info(f"Entered the save object method of MainUtil class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Exited the save object method of MainUtil class")    

    except Exception as e:
        raise SensorException(e, sys)

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file:{file_path} is not exist")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise SensorException(e, sys)

def save_numpy_array_data(file_path:str,array:np.array):
    """
    Save Numpy Array Data to file
    file_path:str Location of file to save
    array:np.array Data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise SensorException(e, sys)

def load_numpy_array_data(file_path:str)->np.array:
    """
    Load Numpy Array Data from file
    file_path:str Location of file to save
    array:np.array Data to save
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise SensorException(e, sys)        


        



