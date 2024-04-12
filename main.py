from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import shutil
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os
import uvicorn

tags_metadata = [
    {
        "name": "upload",
        "description": "Manage uploads. So _fancy_ they have their own docs.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "C:/uploads"  # Define your upload directory in the local C drive

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
@app.post("/upload/", tags=["upload"])
async def upload_files(file: UploadFile):
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
            
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(content={"message": "File uploaded successfully", "file": file.filename})
        
    except Exception as e:
        # Log the error or handle it appropriately
        error_message = f"Error uploading file '{file.filename}': {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)
