from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat import get_response  # Make sure chat.py has this

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_route(request: Request):
    data = await request.json()
    message = data.get("message")
    if not message:
        return {"reply": "Empty message."}
    reply, confidence = get_response(message)
    return {"reply": reply, "confidence": round(float(confidence) * 100, 2)}
