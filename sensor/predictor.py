from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from typing import Optional
from glob import glob # Return all files inside folder
from sensor.entity.config_entity import TEST_FILE_NAME,TRANSFORMER_OBJECT_FILENAME,TARGET_ENCODER_OBJECT_FILE_NAME,MODEL_FILE_NAME

# The main aim of this class take model from save model directory and make a pridiction

class ModelResolver: # Get location of Tranformaer,Model and targetencoder 
    def __init__(self,model_registry:str="saved_models",
                transformer_dir_name="transformer",
                target_encoder_dir_name="target_encoder",
                model_dir_name="model"):

                self.model_registry = model_registry
                os.makedirs(self.model_registry,exist_ok=True)
                self.transformer_dir_name = transformer_dir_name
                self.target_encoder_dir_name = target_encoder_dir_name
                self.model_dir_name = model_dir_name
        

    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
                
            dir_names = list(map(int, dir_names))
            latest_dir_name = max(dir_names)

            return os.path.join(self.model_registry,f"{latest_dir_name}")
            
        except Exception as e:
            raise e

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path() 
            
            if latest_dir is None:
                raise Exception(f'Model is not available')
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_tranformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()  
            if latest_dir is None:
                raise Exception(f'Tranformer is not available')
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILENAME)
            
        except Exception as e:
            raise e 

    def get_latest_targetencoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path() 
            if latest_dir is None:
                raise Exception(f'Target Encoer is not available')
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME) 
            
        except Exception as e:
            raise e

    def get_latest_save_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir==None:
                return os.path.join(self.model_registry,f"{0}")

            latest_dir_number = int(os.path.basename(self.get_latest_dir_path()))

            return os.path.join(self.model_registry,f"{latest_dir_number+1}") 
            
        except Exception as e:
            raise e 

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
            
        except Exception as e:
            raise e   

    def get_latest_save_tranformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path() 
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILENAME)
            
        except Exception as e:
            raise e 

    def get_latest_save_targetencoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path() 
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME) 
            
        except Exception as e:
            raise e       
            

'''
class Predictor:

    def __init__(self,model_resolver:ModelResolver):
        self.model_resolver = model_resolver
    
        '''



# We want Tranformaer,Model and targetencoder pkl file too in single folder

