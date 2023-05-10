from nasa.pipeline.training_pipeline import TrainPipeline
#from fastapi.responses import Response
from nasa.ml.estimator import ModelResolver
from nasa.constant.training_pipeline import SAVED_MODEL_DIR
from nasa.utils.main_utils import load_object
import pandas as pd
#from fastapi import File
#from io import BytesIO
from flask import Flask, Response
import pickle
import dill
import logging


app = Flask(__name__)

@app.route('/')
def home():
    return "App started"

@app.route('/train', methods=['GET','POST'])
def train_route():
    try:
        train_pipeline = TrainPipeline()
        #if train_pipeline.is_pipeline_running:
            #return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return 'Training successful !!'
    except Exception as e:
        return Response("Error Occurred! %s" % e)

@app.route("/uploadfile_predict", methods=['GET','POST'])
def read_csv_file():
    try:
        
        df = pd.read_csv("test_FD002.txt",sep='\s+',header=None,index_col=False)
        #with open('model.pkl', 'rb') as f:
            #load_model = dill.load(f)
        model_resolver = ModelResolver(model_dir = SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path = best_model_path)  

        y_pred = model.predict_df(df)

        df["RUL"] = y_pred

        return Response(df['RUL'].to_csv())
    except Exception as e:
        return Response(f"Error occured! {e}")


if __name__=="__main__":
    #training_pipeline = TrainPipeline()
    #training_pipeline.run_pipeline()
    #uvicorn.run(app, host='127.0.0.1', port=8080)
    app.run(debug=True)