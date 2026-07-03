import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from chat_ai import generate_reply

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Filip Makarczyk | Personal Brand")

# Mount static files if needed
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Landing Page nicht gefunden</h1>", status_code=404)


@app.get("/health")
async def health():
    return {"status": "healthy"}


# ═══════════════════════════════════════════════════════════════════════════════
# KI-Chat – Groq-basiert (siehe chat_ai.py)
# ═══════════════════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.post("/api/chat")
async def chat(payload: ChatRequest, request: Request):
    message = (payload.message or "").strip()
    if not message:
        return JSONResponse({"reply": "Bitte geben Sie eine Nachricht ein."}, status_code=400)
    if len(message) > 2000:
        message = message[:2000]

    # Session-ID vom Client übernehmen, sonst als grobe Notlösung die Client-IP
    # nutzen, damit zumindest kurzer Kontext über mehrere Nachrichten erhalten
    # bleibt (Frontend generiert aktuell keine eigene Session-ID).
    session_id = payload.session_id or (request.client.host if request.client else str(uuid.uuid4()))

    try:
        reply = await generate_reply(session_id, message)
    except Exception:
        logger.exception("Fehler bei /api/chat")
        reply = "Entschuldigung, es gab ein technisches Problem. Bitte versuchen Sie es erneut."

    return {"reply": reply}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
