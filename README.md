# DataFlow_pipeline
A containerized Excel ETL microservice built with FastAPI.
It extracts raw Excel files, transforms them into a consistent format, and returns the cleaned dataset as a new Excel file.

## Features
- Extract: Accept .xlsx uploads through the API
- Transform:
    1. Normalize column names → lowercase, underscores instead of spaces

    2. Convert amounts with commas to numeric ("30,5" → 30.5)

    3. Detect and format date columns (01/03/24 or March 1st 2024 → 01-03-2024)

- Load: Return the transformed file as downloadable Excel (cleaned.xlsx)

Extensible: DuckDB integration, missing values handling, duplicates, outlier detection, CSV integration

*More details will follow* 

