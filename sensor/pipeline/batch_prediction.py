from sensor.exception import SensorException
import os,sys
from sensor.utils import load_object,save_object
from sensor.logger import logging
from sensor.predictor import ModelResolver
import pandas as pd
from datetime import datetime
import numpy as np

PRIDICTION_DIR = "prediction"
#PRIDICTION_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PRIDICTION_DIR,exist_ok=True)

        logging.info(f"Creating Model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading File: {input_file_path}")
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)
       
        # Validation should be there and this is assignment 

        logging.info(f"Loading Tranformer to tranform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_tranformer_path())

        input_feature_name = list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_name])

        logging.info(f"Loading Model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        # Prediction in numerical form so we want to convert it into categorical form
        logging.info(f"Target Encoder to convert predicted column into categorical form")
        target_encoder = load_object(file_path=model_resolver.get_latest_targetencoder_path())
        cat_prediction  = target_encoder.inverse_transform(prediction)

        df["prediction"] = prediction
        df["cat_pred"] = cat_prediction

        
        prediction_file_name = os.path.basename(input_file_path).replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PRIDICTION_DIR,prediction_file_name) 
        df.to_csv(prediction_file_path,index=False,header=True) 

        return prediction_file_path

    except Exception as e:
        raise SensorException(e, sys)