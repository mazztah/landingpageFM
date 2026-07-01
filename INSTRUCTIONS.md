# telllmeeedrei – Bereit für GitHub + Cloud Run Upload

## 1. Dateien in dein bestehendes Repository kopieren

Kopiere folgende Dateien/Ordner in dein Bot-Projekt:

- `Dockerfile` → in den Root deines Projekts
- `static/readme.html` → Ordner `static/` anlegen und Datei hinein
- (Optional) Die `landing_page_v6_fixed.zip` separat nutzen

## 2. Wichtige Änderung in main.py

Füge **am Anfang der Route-Definitionen** (nach den anderen `@app.get` Routen) folgenden Code ein:

```python
from pathlib import Path
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
@app.get("/readme", response_class=HTMLResponse)
async def serve_beautiful_readme():
    """Zeigt die schöne HTML-README als Landing Page"""
    readme_path = Path(__file__).parent / "static" / "readme.html"
    if readme_path.exists():
        return HTMLResponse(readme_path.read_text(encoding="utf-8"))
    
    # Fallback
    return {
        "status": "online",
        "bot": "telllmeeedrei",
        "message": "README nicht gefunden. Bitte static/readme.html anlegen."
    }
```

## 3. GitHub Upload

```bash
git add .
git commit -m "Add beautiful README + optimized Cloud Run Dockerfile"
git push origin main
```

## 4. Cloud Run Deployment

1. Gehe zu Google Cloud Console → Cloud Run
2. "Create Service" → Source Repository auswählen
3. Dockerfile wird automatisch erkannt
4. Wichtige Environment Variables setzen:
   - TELEGRAM_BOT_TOKEN
   - GROQ_API_KEY
   - SUPABASE_URL
   - SUPABASE_KEY
   - (Optional) ANTHROPIC_API_KEY, DASHSCOPE_API_KEY, GEMINI_API_KEY

Fertig! Nach dem Deploy ist deine schöne README unter `https://deine-url.run.app/` erreichbar.

## Zusätzliche Dateien in diesem Paket

- `landing_page_v6_fixed.zip` → Deine Personal Brand Landing Page (separat)
