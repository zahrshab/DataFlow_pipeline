from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import pandas as pd
from transform import run_pipeline
from response import LoggingResponse
from fastapi.responses import StreamingResponse
import io

output_name = "output"
excel_bytes = None

app = FastAPI(title="DataFlow Pipeline")  
@app.post("/process", response_model=LoggingResponse)
async def process_data(file: UploadFile = File(...), output_filename: str = "output"):
    global excel_bytes
    global output_name
    output_name = output_filename
    content = await file.read()
    df = pd.read_excel(io.BytesIO(content))
    
    df = df.copy()
    df_out = run_pipeline(df)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_out.to_excel(writer, index=False, sheet_name="transformed-data")
    
    excel_bytes = output.getvalue() #saving the content bytes
    output.close()
    
    return LoggingResponse(
        rows_in=len(df), rows_out=len(df_out), columns=list(df_out.columns)
    )


@app.get("/download-file")
async def download_file():
    global excel_bytes
    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={output_name}.xlsx"}
    )
    