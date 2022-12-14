from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from typing import Optional
from scipy.stats import ks_2samp 
from scipy import stats
import pandas as pd
import numpy as np
from sensor import utils
from sensor import utils


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
                data_ingestion_artifect:artifact_entity.DataIngestionArtifact):
   
        try:
            logging.info(f"{'>>'*20} Data Validation{'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifect=data_ingestion_artifect
            self.validation_error = dict()

        except Exception as e:
            raise SensorException(e, sys)
                

    def drop_missing_values_column(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
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
            logging.info(f"Selecting column which contain null values above to {thresold}")

            drop_column_names=null_report[null_report>thresold].index
            logging.info(f"Columns to drop {drop_column_names}")


            self.validation_error[report_key_name]=drop_column_names

            df.drop(list(drop_column_names),axis=1,inplace=True)
            if len(df.columns)==0: # Return none if no column left
                return None
            return df    

        except Exception as e:
            raise SensorException(e, sys)

    def is_required_column_exist(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            missing_column=[]
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_col in base_columns:
                if base_col not in current_columns:
                    logging.info(f"column:[{base_col}]is not available")
                    missing_column.append(base_col)


            if len(missing_column)>0:
                self.validation_error[report_key_name]=missing_column  
                return False

            return True

        except Exception as e:
            raise SensorException(e,sys)       

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report= dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution = stats.ks_2samp(base_data,current_data)
                
                
                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    #different distribution




            self.validation_error[report_key_name]=drift_report

        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading Base DataFrame")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace = True)
            logging.info(f"Replace Na value in base DataFrame")

            logging.info(f"Drop Null values column from base DF")  
            base_df=self.drop_missing_values_column(df=base_df,report_key_name="missing_value_within_base_dataset")
           
            logging.info(f"Reading Training DF")
            train_df = pd.read_csv(self.data_ingestion_artifect.train_file_path)
            logging.info(f"Reading Test DF")
            test_df = pd.read_csv(self.data_ingestion_artifect.test_file_path)

            logging.info(f"Drop null values column from Train DF")
            train_df = self.drop_missing_values_column(df=train_df,report_key_name="missing_value_within_train_dataset")
            logging.info(f"Drop null values column from Test DF")
            test_df = self.drop_missing_values_column(df=test_df,report_key_name="missing_value_within_test_dataset")
            
            logging.info(f"Is all required column in Train DF")
            train_df_column_status = self.is_required_column_exist(base_df=base_df, current_df=train_df,report_key_name="missing_column_within_train_dataset")
            logging.info(f"Is all required column in Test DF")
            test_df_column_status = self.is_required_column_exist(base_df=base_df, current_df=test_df,report_key_name="missing_column_within_test_dataset")

            exclude_columns=["class"]
            base_df = utils.convert_column_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_column_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_column_float(df=test_df, exclude_columns=exclude_columns)
             
            if train_df_column_status:
                logging.info(f"As all column are available in Train DF hence deecting data drift")
                #self.data_drift(base_df=base_df, current_df=train_df,report_key_name="Data_dript_within_train_dataset")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")

            if test_df_column_status:
                logging.info(f"As all column are available in Test DF hence deecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="Data_dript_within_test_dataset")
            
        # Write the report   
            logging.info("Write Report in ymal File") 

            utils.write_ymal_file(file_path=self.data_validation_config.report_file_path, 
                                       data=self.validation_error)                                                   

            data_validation_artifect = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)                        
            
            logging.info(f"Data Validation Artifect{data_validation_artifect}")
            return data_validation_artifect
            
        except Exception as e:
            raise SensorException(e, sys)


        

