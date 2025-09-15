from fastapi import FastAPI, File, UploadFile
import pandas as pd
from transform import run_pipeline
from response import LoggingResponse
import io


app = FastAPI()  
@app.post("/process", response_model=LoggingResponse)
async def process_data(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    elif(file.content_type == "json"):
        df = pd.read_json(io.BytesIO(content))
    rows_in = len(df)
    df_out = run_pipeline(df)
    rows_out = len(df_out)
    
    return LoggingResponse(
        rows_in=rows_in, rows_out=rows_out, columns=list(df_out.columns)
    )
    