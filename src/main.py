# IMPORT from Core libraries
from dotenv import load_dotenv
load_dotenv()
# IMPORT from External libraries
from fastapi import FastAPI, File, UploadFile 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# IMPORT from Internal libraries
from lib.mistral.utils import get_answer_from_llm, get_chunks_from_text
from lib.qdrant.utils import get_relevant_points, upload_points, get_point_from_chunk

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    question: str

class textUpload(BaseModel):
    text: str

@app.get("/ping")
def read_root():
    return {"status": "Ok"}

@app.post("/chat/question")
async def ask_chat( query: ChatQuery ):
    context = get_relevant_points( query.question )
    result = get_answer_from_llm( query.question, context )
    return {"result": result}
   
@app.post("/files/binary")
async def index_file( file: UploadFile = File(...) ):
    return {"result": file.filename}

@app.post("/files/text")
async def index_text( body: textUpload ):
    points = []
    
    chunks = get_chunks_from_text( body.text )    
    for chunk in chunks:
        points.append( get_point_from_chunk( chunk ))
    
    upload_points( points )
    return { "chunks": len(chunks) }