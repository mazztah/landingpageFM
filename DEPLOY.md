# telllmeeedrei – Google Cloud Run Deployment

## Schnellstart

1. **Repository auf GitHub hochladen**
2. **In Google Cloud Console → Cloud Run → "Create Service"**
   - Source: GitHub Repository
   - Dockerfile wird automatisch erkannt
3. **Wichtige Environment Variables setzen:**
   - `TELEGRAM_BOT_TOKEN`
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - Optional: `ANTHROPIC_API_KEY`, `DASHSCOPE_API_KEY`, `GEMINI_API_KEY`

## Wichtige Änderungen für Cloud Run

- Die schöne README wird jetzt automatisch unter `/` und `/readme` angezeigt.
- Dockerfile ist optimiert für Cloud Run (User, `/tmp`, dynamischer Port).

## Nach dem Deploy

- Deine Bot-URL: `https://dein-service.run.app`
- README ansehen: `https://dein-service.run.app/readme`
- Telegram Bot ist unter derselben URL erreichbar (Webhook oder Polling)

Viel Erfolg beim Deploy!
