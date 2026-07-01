# Filip Makarczyk Landing Page – Ready for Cloud Run

## Quick Deploy to Google Cloud Run

### 1. Upload to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Landing Page v3"
git remote add origin https://github.com/YOUR_USERNAME/landingpageFM.git
git push -u origin main
```

### 2. Deploy on Cloud Run
1. Go to [Google Cloud Console → Cloud Run](https://console.cloud.google.com/run)
2. Click **"Create Service"**
3. Choose **"Continuously deploy new revisions from a source repository"**
4. Connect your GitHub repo (`landingpageFM`)
5. Select branch `main`
6. Dockerfile will be detected automatically

### 3. Important Environment Variables (optional)
- No special variables needed for basic deployment.

After deployment, your page will be available at:
`https://your-service.run.app`

The beautiful landing page is served at the root `/`.

## Local Testing
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000
