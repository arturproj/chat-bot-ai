import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic

router = APIRouter()

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

class Message(BaseModel):
    role: str
    content: str
 
 
class ChatRequest(BaseModel):
    messages: list[Message]
 
 
@router.post("/chat")
async def chat(req: ChatRequest):

    # Validate the request messages is not empty and the last message has the role "user"
    if not req.messages:
        raise HTTPException(status_code=400, detail='The "messages" field is mandatory.')

    if req.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail='The last message must have the role "user".')
    

    system_prompt = (
        "You are an expert assistant in our field."
        "Always respond in English, in a clear and concise manner."
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": m.role, "content": m.content} for m in req.messages],
        )
    except Exception as exc:
        print(f"Error calling Anthropic API: {exc}")
        raise HTTPException(status_code=500, detail="Error in response generation")

    print(f"Response from Anthropic API: {response}")
    reply = "\n".join(block.text for block in response.content if block.type == "text")


    return {"reply": reply}