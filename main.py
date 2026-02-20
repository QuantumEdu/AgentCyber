"""
CyberGuard — FastAPI Server.

Integra el sistema de agentes ADK con FastAPI.
Expone endpoints custom para chat, listado de agentes y gestion de sesiones.
"""
import os
import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from cyberguard_agents import root_agent

APP_NAME = "cyberguard"
session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_name: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("CyberGuard Multi-Agent System starting...")
    print(f"Agents loaded: {root_agent.name}")
    for sub in root_agent.sub_agents:
        print(f"  - {sub.name}: {sub.description[:60]}...")
    yield
    print("CyberGuard shutting down...")


app = FastAPI(
    title="CyberGuard API",
    description="Sistema Multi-Agente de Ciberseguridad con Google ADK",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "CyberGuard",
        "version": "1.0.0",
        "agents": [root_agent.name] + [a.name for a in root_agent.sub_agents],
        "docs": "/docs",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de chat.
    Envia un mensaje al sistema multi-agente CyberGuard.
    """
    session_id = request.session_id or str(uuid.uuid4())

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=request.user_id,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id,
        )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=request.message)]
    )

    final_response = ""
    agent_name = root_agent.name

    try:
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_response = part.text
                        agent_name = event.author or root_agent.name
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded. Espera 30 segundos e intenta de nuevo."},
            )
        return JSONResponse(
            status_code=500,
            content={"error": f"Error del agente: {error_msg[:200]}"},
        )

    if not final_response:
        final_response = "No se pudo generar una respuesta. Intenta reformular tu consulta."

    return ChatResponse(
        response=final_response,
        session_id=session_id,
        agent_name=agent_name,
    )


@app.get("/agents")
async def list_agents():
    agents = [
        {
            "name": root_agent.name,
            "description": root_agent.description,
            "role": "coordinator",
            "sub_agents": [a.name for a in root_agent.sub_agents],
        }
    ]
    for agent in root_agent.sub_agents:
        tool_names = [t.__name__ if callable(t) else str(t) for t in (agent.tools or [])]
        agents.append({
            "name": agent.name,
            "description": agent.description,
            "role": "specialist",
            "tools": tool_names,
        })
    return {"agents": agents}


@app.delete("/sessions/{user_id}/{session_id}")
async def delete_session(user_id: str, session_id: str):
    await session_service.delete_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    return {"status": "deleted", "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
