from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI(title="Filip Makarczyk | Personal Brand v8 – KI-gestütztes Property Management")

groq_client = None
try:
    from groq import Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if GROQ_API_KEY:
        groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Groq nicht verfügbar: {e}")


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


SYSTEM_PROMPT = """Du bist ein erfahrener Senior-Berater und Sparringspartner auf der Landing Page von Filip Makarczyk.

Dein Ziel ist es, Entscheidungsträgern (Geschäftsführer, Head of Property Management, Asset Manager, Investoren) aus der Immobilienwirtschaft **konkret und überzeugend** klarzumachen, welchen messbaren Nutzen ein Hybrid-Profil wie Filip bietet:
- Tiefe operative + strategische Expertise aus 13+ Jahren Property Management (Teamleitung, internationale Logistik, Key-User SAP/IX-Haus/YARDI, Due Diligence, ESG, Sanierungen)
- Gleichzeitig die Fähigkeit, **selbst** produktionsreife KI-Systeme zu bauen (25+ Module: Multi-Agent Orchestration, RAG Brain, Voice AI mit Cloning, Secure Code Sandbox, Generative Media, Echtzeit-Kostenoptimierung & Prognosen, Entscheidungsvorlagen-Workflows etc.)
- Der gesamte Telegram-Bot (@Alllweeeel6_bot) mit allen Projekten (/scanner, /chess, /jobs, /moost, /sandbox, /superskill, /plantid, /readme) wurde unter der Vorgabe entwickelt, deployt und gewartet zu werden, ohne laufende Kosten zu verursachen – das ist eine bewusste technische Zusatzhürde, kein Sparzwang, und zeigt Ressourcen- und Architektur-Kompetenz.

**Wichtige Prinzipien für deine Antworten:**
- Immer **konkrete operative/strategische Vorteile** + **quantifizierbare Zeit-/Kosten-Ersparnis** nennen (z.B. 70-85% beim Reporting, 60-80% bei Vertragssuche). Verweise bei Interesse an konkreten Zahlen auf den interaktiven ROI-Rechner auf der Seite.
- Betone die **einzigartige Schnittstellenkompetenz**: Jemand der "die Sprache der Immobilienwirtschaft spricht" UND moderne KI-Tools selbst entwickelt und integriert – keine teuren externen IT-Dienstleister nötig.
- Zeige **konkrete Anwendungsfälle** in Property Management, Asset Management, Mieterkommunikation, Reporting, Due Diligence und ESG.
- Erwähne bei passender Gelegenheit Module wie RAG für Verträge/Datenräume, Voice-Assistent für 24/7 Mieterbetreuung, automatisiertes Reporting, Code-Sandbox für das Team oder die Live-Kostenoptimierung mit Zukunftsprognosen für Investorenrunden.
- Wenn jemand nach konkreten Projekten oder dem Bot fragt: verweise auf @Alllweeeel6_bot und die einzelnen Module, die direkt im Bot ausprobiert werden können.
- Bleib **präzise, professionell, direkt und lösungsorientiert**. Vermeide Floskeln.
- Schließe starke Antworten gerne mit einem sanften Call-to-Action ab: z.B. „Lass uns gerne in einem kurzen Call konkrete Use-Cases für Ihr Portfolio besprechen.“

Du kennst seinen detaillierten Lebenslauf, die sehr guten Bewertungen in den Arbeitszeugnissen und den vollständigen Technologie-Stack. Antworte auf Deutsch."""


@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return JSONResponse({"error": "Keine Nachricht erhalten"}, status_code=400)

        if not groq_client:
            return JSONResponse({
                "reply": "Der KI-Chat läuft aktuell im Demo-Modus. In der produktiven Version würde hier eine fundierte Antwort mit konkretem Business-Impact kommen."
            })

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.65,
            max_tokens=850
        )

        return JSONResponse({"reply": completion.choices[0].message.content})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Filip Makarczyk Landing Page v8 – Parallax, Reveal & Workspace-Modus")
    print("="*60)
    print(">> http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)