import os
from pathlib import Path
from google.adk.agents.run_config import StreamingMode
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from google.genai import types
from google.adk.runners import Runner, RunConfig
from db_sessions import get_or_create_session, session_service, APP_NAME
from root.agent import root_agent
from fastapi.staticfiles import StaticFiles



import logging

# Load environment variables
load_dotenv()

config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=200
)

# Create the runner with the root agent
runner_root = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

app = FastAPI()


# Get allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS')


# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class SessionInitRequest(BaseModel):
    session_id: str

class SessionInitResponse(BaseModel):
    status: str
    session_id: str


def handle_stream_event(event):
    """Helper to process a single event and yield appropriate output."""
    if getattr(event, "partial", False):
        if event.content and event.content.parts:
            print(event.content.parts[0].text)
            return event.content.parts[0].text
        elif event.actions and event.actions.escalate:
            msg = f"Agent escalated: {event.error_message or 'No specific message.'}"
            print(msg)
            return f"data: {msg}"
    return None

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    session_id = request.session_id
    user_id = f"user_{session_id}"
    content = types.Content(role='user', parts=[types.Part(text=request.message)])
    print(f"Received User Message: {request.message} for session: {session_id}")

    async def event_generator():
        try:
            async for event in runner_root.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
                run_config=config,
            ):
                result = handle_stream_event(event)
                if result is not None:
                    yield result
                if event.is_final_response():
                    break
        except Exception as e:
            logging.error(f"Error during streaming: {str(e)}")
            yield "An error occurred while processing your request."

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/session/init", response_model=SessionInitResponse)
async def session_init(request: SessionInitRequest = Body(...)):
    logging.info(f"Initializing session: {request.session_id} for user: user_{request.session_id}")
    user_id = f"user_{request.session_id}"
    # Prepare state dict for session
    state = {
        "session_id": request.session_id  # <-- Save to state
    }
    # Create or get the session with state
    session = await get_or_create_session(user_id=user_id, session_id=request.session_id, state=state)
    print(f"Session created with ID: {session.id} and state: {session.state}")
    return SessionInitResponse(status="created", session_id=request.session_id)


app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)