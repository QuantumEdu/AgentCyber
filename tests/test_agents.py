"""Test rapido del sistema CyberGuard."""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from cyberguard_agents import root_agent


async def test_chat(message: str, session_id: str = "test-001"):
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="cyberguard_test",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="cyberguard_test",
        user_id="tester",
        session_id=session_id,
    )

    content = types.Content(role="user", parts=[types.Part(text=message)])

    print(f"\n{'='*60}")
    print(f"Pregunta: {message}")
    print(f"{'='*60}")

    async for event in runner.run_async(
        user_id="tester",
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    print(f"  Tool call: {part.function_call.name}({part.function_call.args})")
                if hasattr(part, 'function_response') and part.function_response:
                    print(f"  Tool response received")

        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"\nRespuesta ({event.author}):")
                print(event.content.parts[0].text)


async def main():
    test_cases = [
        # CIS Advisor
        ("Cuales son los controles CIS de SSH para Linux?", "test-cis"),
        # Port Scanner (nmap real)
        ("Escanea los puertos de scanme.nmap.org", "test-scan"),
        # Incident Responder
        ("Recibimos un email con un enlace sospechoso y un empleado dio sus credenciales", "test-incident"),
        # Recon - DNS
        ("Haz una consulta DNS de google.com", "test-dns"),
        # Recon - HTTP Headers
        ("Analiza los headers de seguridad de https://example.com", "test-headers"),
    ]

    for message, session_id in test_cases:
        await test_chat(message, session_id)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
