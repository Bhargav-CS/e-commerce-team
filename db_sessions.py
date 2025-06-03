# Choose session backend based on environment/config
import os
from typing import Dict
from google.adk.sessions import InMemorySessionService, DatabaseSessionService



SESSION_BACKEND = os.getenv("SESSION_BACKEND", "memory")  # 'memory' or 'db'

if SESSION_BACKEND == "db":
    db_url = os.getenv("SESSION_DB_URL", "sqlite:///./agents.db")
    session_service = DatabaseSessionService(db_url=db_url)
else:
    session_service = InMemorySessionService()

APP_NAME = "multi_agent"



# Store active sessions only for in-memory backend
active_sessions: Dict[str, dict] = {} if SESSION_BACKEND == "memory" else None

# --- Session Management Helpers ---
import asyncio

async def get_or_create_session(user_id: str, session_id: str, state: dict = None):
    if SESSION_BACKEND == "memory":
        if session_id not in active_sessions:
            session = session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id,
                state=state or {
                    'session_id': session_id
                }
            )
            active_sessions[session_id] = {
                "user_id": user_id,
                "session": session
            }
        return active_sessions[session_id]["session"]
    else:
        # For DB, always try to get, else create
        sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
        for s in sessions:
            if getattr(s, 'id', None) == session_id:
                return s
        # Not found, create
        return await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state=state or {
                'session_id': session_id
            }
        )

async def get_session(user_id: str, session_id: str):
    if SESSION_BACKEND == "memory":
        session_info = active_sessions.get(session_id)
        if session_info and session_info["user_id"] == user_id:
            return session_info["session"]
        return None
    else:
        sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
        for s in sessions:
            if getattr(s, 'id', None) == session_id:
                return s
        return None

async def delete_session(user_id: str, session_id: str):
    if SESSION_BACKEND == "memory":
        session_info = active_sessions.get(session_id)
        if session_info and session_info["user_id"] == user_id:
            del active_sessions[session_id]
            return True
        return False
    else:
        await session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        return True

async def list_sessions(user_id: str):
    if SESSION_BACKEND == "memory":
        return [sid for sid, info in active_sessions.items() if info["user_id"] == user_id]
    else:
        sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
        return [s.id for s in sessions]