from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from typing import Optional
from scipy import ks_2samp
import pandas as pd


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation"{'<<'*20})
            self.data_validation_config = data_validation_config
            self.validation_error = dict()

        except Exception as e:
            raise SensorException(e, sys)
                

    def drop_missing_values_column(self,df:pd.DataFrame)->Optional[pd.DataFrame]:
        """
        ======================================================================
        This function will drop a column which has more than 30 % null values

        df:Accept a pandas DataFrame 
        thresold: percent criteria to drop a column
        =======================================================================
        return panda df if at least single column is available after missing column
        """
        try:
            thresold=self.data_validation_config.missing_thresold
            '''
            drop_column_name=[]
            for column_name,missing_percentage in zip((df.isnull().sum()/df.shape[0]).index ,(df.isnull().sum()/df.shape[0]).values):
                if missing_percentage>0.3:
                    drop_column_name.append(column_name)
            '''
            null_report=df.isna().sum()/df.shape[0]
            drop_column_names=null_report[null_report>thresold].index

            self.validation_error["dropped_columns"]=drop_column_names

            df.drop(list(drop_column_names),axis=1,inplace=True)
            if len(df.columns)==0: # Return none if no column left
                return None
            return df    

        except Exception as e:
            raise SensorException(e, sys)

    def is_required_column_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame)->bool:
        try:
            missing_column=[]
            base_columns = base_df.columns
            current_columns = current_column.column

            for base_col in base_columns:
                if base_col not in current_columns:
                    missing_column.append(base_col)


            if len(missing_column)>0:
                self.validation_error["missing_columns"]=missing_column  
                return False

            return True

        except Exception as e:
            raise SensorException(e,sys)       


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        pass

