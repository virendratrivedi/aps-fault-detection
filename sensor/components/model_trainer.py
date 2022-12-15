from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.config import TARGET_COLUMN
import os,sys
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score

class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifect:artifact_entity.DataTransformationArtifact
                ):
                try:

                    logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
                    self.model_trainer_config=model_trainer_config
                    self.data_transformation_artifect=data_transformation_artifect
                    
                except Exception as e:
                    raise SensorException(e, sys)

    def fineTune_model(self):
        try:
         pass
        except Exception as e:

            raise SensorException(e, sys)

    def train_model(self,x,y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading Train and Test Array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifect.transform_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifect.transform_test_path)
            
            logging.info(f"Splitting Input and Target Feature from Train and test Array")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]
            
            logging.info(f"Train The Model")
            model = self.train_model(x=x_train,y=y_train)
             
            logging.info(f"Calculating F1 Train Score") 
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)
            
            logging.info(f"Calculating F1 Test Score") 
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)

            # Check for overfitting and underfitting or expected score
            logging.info(f"Checking our Model Underfitting or not") 
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good.Not Expected Accuracy:{self.model_trainer_config.expected_score} model Actual Score is: {f1_test_score}")
            logging.info(f"F1 Triain Score:{f1_train_score} and F1 test Score:{f1_test_score}")

            logging.info(f"Checking our Model Overfiting or not")  
            diff = abs(f1_train_score,f1_test_score)   
            if diff>self.model_trainer_config.overfiting_thresold:
                raise Exception(f"Model is overfiting:{self.model_trainer_config.overfiting_thresold} difference is: {diff}")

            logging.info(f"Saving Model Object")  
            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)    

            # Prepare Artifect
            logging.info(f"Prepare Model Artifect")  
            model_trainer_artifect = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
                     f1_train_score=f1_train_score, f1_test_score=f1_test_score)

            logging.info(f"Model Trainer Artifect: {model_trainer_artifect}")
            return model_trainer_artifect         

        except Exception as e:
            raise SensorException(e, sys)

                    




                
              
            

        