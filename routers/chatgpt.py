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
    
    if not isinstance(req.messages, list):
        raise HTTPException(status_code=400, detail='The "messages" field must be a list.')

    if req.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail='The last message must have the role "user".')
    

    system_prompt = (
        "Sei un assistente esperto del nostro settore. "
        "Rispondi sempre in italiano, in modo chiaro e conciso."
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": m.role, "content": m.content} for m in req.messages],
        )
    except Exception as exc:
        print(f"Errore chiamata Anthropic API: {exc}")
        raise HTTPException(status_code=500, detail="Errore nella generazione della risposta")
 
    print(f"Response from Anthropic API: {response}")
    reply = "\n".join(block.text for block in response.content if block.type == "text")


    return {"reply": reply}