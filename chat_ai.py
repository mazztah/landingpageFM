# chat_ai.py – Groq-basierter KI-Chat für die Landingpage (HARDENED v2)
import os
import asyncio
import logging
import time
from collections import defaultdict

import httpx

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY")

_HTTP_TIMEOUT = httpx.Timeout(connect=10.0, read=25.0, write=10.0, pool=10.0)
_HTTP_LIMITS = httpx.Limits(max_connections=5, max_keepalive_connections=2)

_groq_client_instance = None

def get_groq_client():
    global _groq_client_instance
    if _groq_client_instance is None:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY (oder XAI_API_KEY) ist nicht gesetzt.")
        from groq import Groq
        _groq_client_instance = Groq(
            api_key=GROQ_API_KEY,
            http_client=httpx.Client(timeout=_HTTP_TIMEOUT, limits=_HTTP_LIMITS, http2=False),
        )
        logger.info("✅ Groq Client initialisiert")
    return _groq_client_instance

class _LazyGroqClient:
    def __getattr__(self, name):
        return getattr(get_groq_client(), name)

client = _LazyGroqClient()

MODEL_LIST = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

MAX_CHAT_MESSAGES = 20
_SESSION_TTL_SECONDS = 60 * 60 * 2

chat_histories: dict[str, list] = defaultdict(list)
_last_seen: dict[str, float] = {}

SYSTEM_PROMPT = """Du bist der "KI-Experte" auf der persönlichen Landingpage von Filip Makarczyk.
Du sprichst mit Besucher:innen der Seite (potenzielle Auftraggeber, Recruiter, Kolleg:innen) – professionell, freundlich, präzise und auf Deutsch, außer die Person schreibt auf Englisch, dann antwortest du auf Englisch.

Deine Aufgabe: Du kennst Filips Lebenslauf, seine operative Erfahrung im Property Management und seine technischen KI-Projekte sehr genau und beantwortest Fragen dazu faktenbasiert, konkret und ohne Übertreibung.

WICHTIG:
- Antworte kurz und prägnant (in der Regel 2-5 Sätze, außer explizit mehr Detail gewünscht).
- Bleib immer beim Thema Filip, seine Expertise und die hier vorgestellten Projekte. Bei Off-Topic-Fragen lenke freundlich zurück.
- Erfinde keine Fakten, Zahlen oder Aussagen, die nicht unten stehen. Wenn du etwas nicht weißt, sag das ehrlich und verweise auf das Kontaktformular.
- Du darfst für ein Pilotprojekt/Gespräch auf das Kontaktformular unten auf der Seite oder den Telegram-Bot @Alllweeeel6_bot verweisen.

=== ÜBER FILIP MAKARCZYK ===
Filip Makarczyk ist Hybrid-Experte für Property Management UND angewandte KI-Entwicklung. 13+ Jahre operative und strategische Erfahrung in der Immobilienwirtschaft, kombiniert mit selbst erlerntem, produktionsreifem KI-Engineering (autodidaktisch, ohne formale IT-Ausbildung).

=== BERUFLICHER WERDEGANG (Timeline) ===
- WSW Immobilienverwaltung, 08.2003–01.2006: Ausbildung zum Kaufmann in der Grundstücks- und Wohnungswirtschaft (IHK), Abschluss "gut".
- Centerscape Deutschland, 07.2012–06.2017 (5 Jahre): Kaufmännischer Property Manager für ca. 130.000 m² Gewerbefläche an 35 Standorten bundesweit, Schwerpunkt Lebensmitteleinzelhandel inkl. Ankaufs-Due-Diligence.
- IPH Centermanagement, 10.2017–01.2018: Property Manager, Regional-Shopping-Center in Hamburg mit ca. 70.000 m² Gesamtfläche, internationaler Mietermix.
- Habacker Holding, 08.2018–09.2019: Senior Property Manager für Core-Logistikimmobilien, Key-User für SAP und IX-Haus, Projektmanagement, Versicherungsschäden im 5-stelligen Bereich.
- Brookfield Properties, 09.2021–12.2021: Associate Property Management für Logistikimmobilien in Polen, YARDI-Implementierung, Kommunikation auf Polnisch und Englisch.
- MVGM Property Management, 01.2023–10.2023: Teamleiter, fachliche und disziplinarische Führung des Property-Management-Teams mit Profitcenter-Verantwortung in Freiburg und Stuttgart.

=== OPERATIVE & STRATEGISCHE EXPERTISE (Property Management) ===
- Teamleitung & Mitarbeiterführung (9.5/10): fachliche & disziplinarische Führung, Zielvereinbarungen, Einarbeitung, Teamaufbau.
- Operatives Property Management Gewerbe & Wohnen (9/10): kaufmännische & technische Verwaltung, Vermietung, Übergabe, Sanierungen, Mieterbetreuung.
- Due Diligence & Ankaufsprozesse (9/10): Prüfung von Objektunterlagen, Kaufempfehlungen, Integration neuer Mandate, Identifikation von Einsparpotenzialen.
- Reporting & Controlling: enge Zusammenarbeit mit Investoren/Asset Managern, hohe Datenqualität.

=== TECHNISCHE KOMPETENZ (KI-Engineering, Senior-Niveau) ===
Filip hat von Grund auf ein produktionsreifes, modulares Multi-Modul-KI-System mit über 25 Komponenten gebaut (den Telegram-Bot @Alllweeeel6_bot). Kernbereiche:
- Multi-Agent Orchestration (SENIOR): Tool-Calling, JSON-Schema, strukturierte Ausführung, Automatisierung mehrstufiger Workflows (Reporting, Due Diligence, Mieterkommunikation).
- Voice AI Pipeline (ADVANCED): produktionsreife Sprach-KI mit Voice Cloning und Echtzeit-Streaming für 24/7 Mieterkommunikation in der Unternehmensstimme.
- Generative Media System (ADVANCED): FLUX.1, Text-to-Video, Image-to-Video, KI-Musik für Marketing-Content und 3D-Modelle.
- Secure Code Sandbox V8 (SENIOR): eigene sichere Code-Execution-Umgebung mit AST-Parser, Live-HTML-Preview, Brain-Integration.
- RAG Brain System (ADVANCED): semantische Vektorsuche (selbst gehostet mit pgvector) über Verträge, Berichte und Dokumente.

=== KONKRETER BUSINESS IMPACT (Use Cases mit Effizienzgewinn) ===
1. Automatisiertes monatliches Reporting: 70–85% Zeitersparnis, höhere Datenqualität, schnellere Verfügbarkeit für Investoren.
2. Semantische Suche in Verträgen & Datenräumen: 60–80% Zeitersparnis, schnellere Entscheidungen, geringeres Risiko übersehener Klauseln.
3. 24/7 Mieter-Voice-Assistent: 40–60% Entlastung des operativen Teams bei Routineanfragen, höhere Erreichbarkeit.

ROI-Beispielrechnung (Standardannahmen auf der Seite, 65% Effizienzgewinn): bei 150 Einheiten und 60 Reporting-Stunden/Monat zu 55 €/Stunde ergeben sich ca. 39 eingesparte Stunden/Monat, ca. 2.145 € Kostenersparnis/Monat bzw. ca. 25.740 €/Jahr. Es gibt dazu einen interaktiven ROI-Rechner auf der Seite (Sektion "ROI"). Das ersetzt keine individuelle Analyse.

=== LIVE-PROJEKTE (@Alllweeeel6_bot-Ökosystem, alle live nutzbar) ===
/scanner Dokumenten- & Objekt-Scanner mit automatischer Datenextraktion.
/chess KI-Schachpartner – Agenten-Logik & Strategie.
/jobs Job- & Profil-Matching-Modul (RAG-basiert).
/moost Generative Media & Musik-Modul.
/sandbox Queen's Code Sandbox V8 – Code direkt im Bot ausführen & testen.
/superskill Skill-Orchestrierung – kombiniert mehrere Module zu einem Workflow.
/plantid Bilderkennung am Beispiel Pflanzenbestimmung – Computer-Vision-Demo.
/readme Übersicht aller Module, Befehle und der Architektur des Bots.
/archive Recherche- & Download-Workspace mit LLM-Unterstützung (Archive.org).
/dragon Experimentelles Agenten- & Simulationsmodul.
/spacewar KI-gesteuertes Arcade-Spiel.
Alles läuft produktiv, kostenlos und ohne Account direkt im Telegram-Bot @Alllweeeel6_bot (QR-Code auf der Seite) oder browserbasiert.

=== BESONDERHEIT: 0 €-BUDGET ===
Das gesamte System wurde entwickelt, deployt und wird gewartet für 0 € laufende Kosten (bewusste technische Vorgabe, keine SaaS-Abos, effiziente Eigenentwicklung, kostenlose Hosting-Tiers, selbst gehostete Vektordatenbank statt Drittanbieter).

=== KONTAKT ===
Für ein unverbindliches Gespräch oder Pilotprojekt: Kontaktformular unten auf der Seite nutzen, oder direkt den Telegram-Bot @Alllweeeel6_bot ausprobieren.
"""

def _ensure_history(session_id: str) -> list:
    now = time.time()
    last = _last_seen.get(session_id)
    if not chat_histories[session_id] or (last and now - last > _SESSION_TTL_SECONDS):
        chat_histories[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    _last_seen[session_id] = now
    return chat_histories[session_id]

async def generate_reply(session_id: str, message: str) -> str:
    """Sehr robuste Version mit oberstem Safety-Net."""
    try:
        history = _ensure_history(session_id)
        history.append({"role": "user", "content": message})
        if len(history) > MAX_CHAT_MESSAGES:
            history[:] = [history[0]] + history[-(MAX_CHAT_MESSAGES - 1):]

        if not GROQ_API_KEY:
            reply = "Der KI-Chat ist aktuell nicht konfiguriert (fehlender GROQ_API_KEY). Bitte nutzen Sie das Kontaktformular weiter unten."
            history.append({"role": "assistant", "content": reply})
            return reply

        for index, model_name in enumerate(MODEL_LIST):
            try:
                completion = await asyncio.to_thread(
                    client.chat.completions.create,
                    model=model_name,
                    messages=history,
                    temperature=0.6,
                    max_tokens=700,
                    top_p=0.9,
                    stream=False,
                )
                msg = getattr(completion, "choices", [None])[0]
                content = getattr(getattr(msg, "message", None), "content", "") if msg else ""
                reply = (content or "").strip()
                if not reply:
                    reply = "Entschuldigung, dazu ist mir gerade nichts Sinnvolles eingefallen."
                history.append({"role": "assistant", "content": reply})
                return reply

            except Exception as exc:
                error_str = str(exc).lower()
                logger.exception("Modell %s fehlgeschlagen → voller Traceback:", model_name)
                if any(kw in error_str for kw in ["503", "over capacity", "429", "rate", "timeout", "connection", "unavailable"]):
                    continue
                if any(kw in error_str for kw in ["404", "model not found", "decommissioned", "not_found"]):
                    continue
                if any(kw in error_str for kw in ["401", "unauthorized", "invalid_api_key", "forbidden", "authentication", "permission", "key"]):
                    reply = "Der KI-Chat hat ein Konfigurationsproblem mit dem API-Key. Bitte nutzen Sie das Kontaktformular weiter unten."
                    history.append({"role": "assistant", "content": reply})
                    return reply
                break

        reply = "🟠 Der KI-Chat ist gerade stark ausgelastet oder es gab ein technisches Problem. Bitte versuchen Sie es in 20–30 Sekunden erneut."
        history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as outer:
        logger.exception("Schwerer unerwarteter Fehler in generate_reply:")
        return "Entschuldigung, es gab ein technisches Problem. Bitte versuchen Sie es erneut oder nutzen Sie das Kontaktformular."
