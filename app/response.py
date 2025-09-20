from pydantic import BaseModel

class LoggingResponse(BaseModel):
    rows_in:int
    rows_out:int
    columns:list[str]