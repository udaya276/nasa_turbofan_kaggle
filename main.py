from nasa.pipeline.training_pipeline import TrainPipeline
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.responses import Response
import uvicorn
from nasa.ml.estimator import ModelResolver
from nasa.constant.training_pipeline import SAVED_MODEL_DIR
from nasa.utils.main_utils import load_object
import pandas as pd
from fastapi import File
from io import BytesIO




app = FastAPI()
"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
@app.get("/", tags=["authentication"])
async def index():
    #return {"App started"}
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        #if train_pipeline.is_pipeline_running:
            #return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occured! {e}")
  
@app.post("/uploadfile_predict/")
async def upload_csv_file(file: UploadFile = File(...)):
    try:
        #return {"filename": file.filename}
        #df = pd.read_csv(file.file)
        contents = file.file.read()
        buffer = BytesIO(contents)
        df = pd.read_csv(buffer, sep='\s+',header=None,index_col=False)
        #return df.head(10)
        model_resolver = ModelResolver(model_dir = SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path = best_model_path)
        y_pred = model.predict_df(df)
        df["RUL"] = y_pred
        return df["RUL"]
    except Exception as e:
        return Response(f"Error occured! {e}")


if __name__=="__main__":
    #training_pipeline = TrainPipeline()
    #training_pipeline.run_pipeline()
    uvicorn.run(app, host='127.0.0.1', port=8080)