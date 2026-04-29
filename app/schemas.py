from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class UploadRequest(BaseModel):
    path: str