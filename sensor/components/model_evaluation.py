from sensor.predictor import ModelResolver
from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
import os,sys

class ModelEvaluation:

    def __init__(self,model_evel_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifect:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifect:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifect:artifact_entity.ModelTrainerArtifact):
                 try:
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
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_evel_artifect = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
                improve_accuracy=None)
                return model_evel_artifect
        except Exception as e:
            raise SensorException(e,sys)                

                                    

                    
                    
                

                 
                        
                
                




    
    


