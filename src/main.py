# IMPORT from Core libraries
from dotenv import load_dotenv
load_dotenv()
# IMPORT from External libraries
from fastapi import FastAPI, File, UploadFile 
from pydantic import BaseModel
# IMPORT from Internal libraries

app = FastAPI()

@app.get("/ping")
def status_ping():
    return {"status": "Ok"}
