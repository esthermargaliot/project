from fastapi import FastAPI
from pydantic import BaseModel
from openai_service import openai_chat_completion

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Request body model
class MessageRequest(BaseModel):
    message: str


@app.post("/completion")
async def message(request: MessageRequest):
    return await openai_chat_completion(request.message)