'''from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
import sys,os
from sensor.components.model_trainer import ModelTrainer
from sensor.components.data_transformation import DataTransformation
from sensor.entity import config_entity
from sensor.components import data_ingestion
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher'''
from sensor.pipeline.training_pipiline import start_training_pipiline
from sensor.exception import SensorException
import os,sys
from sensor.pipeline.batch_prediction import start_batch_prediction

file_path="/config/workspace/aps_failure_training_set1.csv"
def test_looging_and_exception():
     try:
          logging.info("starting the test and logger function")
          result=2/0
          print(result)
          logging.info("stoping the test and logger function")
     except Exception as e:
          logging.debug("stoping the test and logger function")
          raise SensorException(e, sys)

if __name__=='__main__':
     try:
          
          #start_training_pipiline()
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)
     except Exception as e:
          raise SensorException(e, sys)
     '''
     try:
          #test_looging_and_exception()
          #get_collection_as_dataframe(database_name='aps', collection_name='sensor')

          # Data ingestion
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          # Data Validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,
                                             data_ingestion_artifect=data_ingestion_artifact)

          data_validation_artifect = data_validation.initiate_data_validation()  

          # Data Transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
                                                    data_ingestion_artifect=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()   

          # Model Trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)   
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, 
                                       data_transformation_artifect=data_transformation_artifact)   
          
          model_trainer_artifact = model_trainer.initiate_model_trainer() 

          # Model Evaluation
          model_evel_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config) 
          model_evel = ModelEvaluation(model_evel_config=model_evel_config, data_ingestion_artifect=data_ingestion_artifact, 
                        data_transformation_artifect=data_transformation_artifact, 
                        model_trainer_artifect=model_trainer_artifact)
          
          model_evel_artifect = model_evel.initiate_model_evaluation()  

          # Model Pusher
          model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)
          model_pusher=ModelPusher(model_pusher_config=model_pusher_config, 
                                   data_transformation_artifact=data_transformation_artifact, 
                                   model_trainer_artifact=model_trainer_artifact)

          model_pusher_artifact = model_pusher.initiate_model_pusher()   



                                      
          
     except Exception as e:
          raise SensorException(e, sys)
                   
'''

'''
import pymongo

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

# Database Name
dataBase = client["neurolabDB"]

# Collection  Name
collection = dataBase['Products']

# Sample data
d = {'companyName': 'iNeuron',
     'product': 'Affordable AI',
     'courseOffered': 'Machine Learning with Deployment'}

# Insert above records in the collection
rec = collection.insert_one(d)

# Lets Verify all the record at once present in the record with all the fields

all_record = collection.find()

# Printing all records present in the collection
for idx, record in enumerate(all_record):
     print(f"{idx}: {record}")
'''