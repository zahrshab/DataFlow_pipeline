from pydantic import BaseModel
from typing import List

class LoggingResponse(BaseModel):
    rows_in:int
    rows_out:int
    columns:list[str]
