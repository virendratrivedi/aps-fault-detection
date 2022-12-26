from sensor.predictor import ModelResolver
from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
import pandas as pd
import os,sys
from sensor.logger import logging
from sensor.utils import load_object
from sklearn.metrics import f1_score
from sensor.config import TARGET_COLUMN

class ModelEvaluation:

    def __init__(self,model_evel_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifect:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifect:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifect:artifact_entity.ModelTrainerArtifact):
                 try:
                    logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")

                    self.model_evel_config = model_evel_config
                    self.data_ingestion_artifect = data_ingestion_artifect
                    self.data_transformation_artifect = data_transformation_artifect
                    self.model_trainer_artifect = model_trainer_artifect
                    self.model_resolver = ModelResolver()

                 except Exception as e:
                    raise SensorException(e, sys)


    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # IF saved Model have Models then we will compare which Model is best. 
            # Trained or Model from saved_folder
            logging.info("IF saved Model have Models then we will compare which Model is best"
            "Trained or Model from saved_folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
                improve_accuracy=None)
                logging.info(f"Model Evaluation Artifect: {model_eval_artifact}")
                return model_eval_artifact
               
            # Finding location of Tranformer,Model and Target Encoder  
            logging.info("Finding location of Tranformer,Model and Target Encoder") 
            transformer_path = self.model_resolver.get_latest_tranformer_path()  
            model_path = self.model_resolver.get_latest_model_path()
            targetencoder_path = self.model_resolver.get_latest_targetencoder_path()
            
            # Previously Trainer Objects. Outside from Training Pipeline
            logging.info("Previously Trainer Objects. Outside from Training Pipeline") 
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=targetencoder_path)
           
           # In model trainer artifect we have current trained Model.This is currently Trained Model Objects
           # Getting from your training pipiline
            logging.info("In model trainer artifact we have current trained Model.This is currently Trained Model Objects"
            "Getting from your training pipiline")
            current_tranformer = load_object(file_path=self.data_transformation_artifect.transformation_object_path)
            current_model = load_object(file_path=self.model_trainer_artifect.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifect.target_encoder_path)

           # We will do comparision in test dataset
             
            test_df = pd.read_csv(self.data_ingestion_artifect.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_encoder.transform(target_df)
           # Accuracy using previosuly Trained Model 
            logging.info("Accuracy using previosuly Trained Model ") 
            input_arr = transformer.transform(test_df) 
            y_pred = model.predict(input_arr)
            print(f"Pridiction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previosuly Trained Model:{previous_model_score}") 

           # Accuracy Using current train Model
            
            input_arr = current_tranformer.transform(test_df)
            y_pred = current_model.predict(input_arr)
            y_true = current_target_encoder.transform(target_df)
            print(f"Pridiction using Trained model: {current_target_encoder.inverse_transform(y_pred[:7])}")
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using Current Trained Model:{current_model_score}") 

            if current_model_score<previous_model_score:
                logging.info(f"Current Trained Model is not greater than previous Model") 
                raise Exception("Current Trained Model is not greater than previous Model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
                                   improve_accuracy=current_model_score-previous_model_score)  
            
            logging.info(f"model_eval_artifact: {model_eval_artifact} ")
            return model_eval_artifact
            

        except Exception as e:
            raise SensorException(e,sys)                

                                    

                    
                    
                

                 
                        
                
                




    
    


