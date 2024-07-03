from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai_handler import text_handler
from models import MercorUsers, Message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/query", response_model=List[Message])
async def read_item(messages: List[Message]):
    try:
        # messages from List[Message] to List[Dict[str, str]]
        messages = [
            message.model_dump() for message in messages if message.role != "system"
        ]
        response = text_handler(messages)

        if response:
            return response
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
