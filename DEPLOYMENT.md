# 🌿 Mosaic Trends Radar — Deployment Guide

## Architecture

```
mosaic-trends-radar/
├── frontend/          ← Next.js 14 → Deploy to Vercel
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx       ← Dashboard with Radar Scan
│   ├── components/
│   │   ├── RadarChart.tsx   ← Recharts radar visualization
│   │   ├── TrendCard.tsx    ← Opportunity card per trend
│   │   ├── ScanButton.tsx   ← Animated scan trigger
│   │   └── StatusLog.tsx    ← Live pipeline log stream
│   ├── styles/globals.css
│   ├── package.json
│   ├── vercel.json          ← Vercel config (Next.js only, no Python)
│   └── .env.local           ← NEXT_PUBLIC_API_URL
│
└── backend/           ← Python Flask → Deploy to Railway
    ├── app.py               ← Flask API (POST /scan, GET /health)
    ├── trend_engine.py      ← Pipeline orchestrator
    ├── data_ingestion/
    │   ├── google_trends.py ← PyTrends + fallback data
    │   ├── reddit_signals.py← Reddit JSON API (no auth needed)
    │   └── pubmed_signals.py← NCBI E-utilities (free)
    ├── analysis/
    │   └── scorer.py        ← Multi-factor trend scoring
    ├── requirements.txt     ← No heavy ML deps (no torch/CUDA)
    ├── Procfile             ← gunicorn for Railway
    └── railway.json         ← Railway deployment config
```

---

## STEP 1 — Push to GitHub

```bash
# Replace the repo with the restructured version:
git clone https://github.com/jainkriti907-max/mosaic-trends-radar temp-clone
cp -r frontend backend .gitignore temp-clone/
cd temp-clone

# Remove the old mixed files
rm -rf components pages services styles
rm -f package.json next.config.js tailwind.config.js tsconfig.json
rm -f postcss.config.js vercel.json .vercelignore .env.example

git add -A
git commit -m "restructure: split frontend/backend, fix Vercel deployment"
git push origin main
```

---

## STEP 2 — Deploy Frontend to Vercel

### Option A: Vercel Dashboard (Recommended)
1. Go to https://vercel.com/new
2. Import `jainkriti907-max/mosaic-trends-radar`
3. **Set Root Directory to `frontend`**
4. Framework: Next.js (auto-detected)
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = *(leave blank for now, update after backend deploys)*
6. Click Deploy

### Option B: Vercel CLI
```bash
npm install -g vercel
cd frontend
vercel --prod
# Answer prompts:
#   Root directory? frontend (or . if you cd'd in)
#   Framework? Next.js
```

---

## STEP 3 — Deploy Backend to Railway

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select `jainkriti907-max/mosaic-trends-radar`
4. **Set Root Directory to `backend`**
5. Railway auto-detects Python + Procfile
6. Add environment variable:
   - `FRONTEND_URL` = your Vercel URL (e.g. `https://mosaic-trends-radar.vercel.app`)
7. Deploy → Railway will give you a URL like `https://mosaic-trends-radar-production.up.railway.app`

---

## STEP 4 — Connect Frontend to Backend

1. Copy your Railway backend URL
2. Go to Vercel → Project Settings → Environment Variables
3. Add/update:
   - `NEXT_PUBLIC_API_URL` = `https://your-app.up.railway.app`
4. Redeploy frontend (Deployments → Redeploy)

---

## STEP 5 — Verify

Test the backend directly:
```bash
curl -X POST https://your-railway-url.up.railway.app/scan \
  -H "Content-Type: application/json" \
  -d '{"category": "wellness", "region": "IN"}'
```

Expected response:
```json
{
  "success": true,
  "count": 10,
  "trends": [
    {
      "name": "Berberine",
      "score": 82,
      "classification": "Strong Trend",
      "marketOpportunity": "$420M by 2028",
      "productConcept": "Berberine + chromium metabolic support capsules",
      "packagingFormat": "Eco-pack capsules with 90-day supply",
      "launchTiming": "Q2 2025 — summer metabolic trend",
      "opportunityBrief": "...",
      "signals": {
        "velocity": 76,
        "marketPotential": 80,
        "scientificBacking": 84,
        "consumerBuzz": 74,
        "competition": 30
      }
    },
    ...
  ]
}
```

---

## Data Sources

| Source | Method | Auth Required |
|--------|--------|--------------|
| Google Trends | PyTrends library | None |
| Reddit | Public JSON API | None |
| PubMed | NCBI E-utilities | None |
| YouTube | (in scoring signals) | None |
| Ecommerce | (in calibrated scores) | None |

The system uses live data where available and intelligently falls back to
calibrated real-world data if an API is rate-limited or unavailable.

---

## Why This Architecture Works

**Old (broken):**
```
repo-root/
├── components/      ← Next.js
├── pages/           ← Next.js  
├── services/        ← Python ← Vercel tried to install torch + CUDA → FAIL
├── package.json     ← references Python scripts
└── vercel.json      ← no clear framework separation
```

**New (fixed):**
```
repo-root/
├── frontend/        ← Vercel only sees this (pure Next.js, zero Python)
│   └── vercel.json  ← framework: nextjs, no Python build steps
└── backend/         ← Railway only sees this (pure Python, no Node.js)
    └── railway.json ← gunicorn startup, Python 3.11
```

Vercel's `Root Directory: frontend` setting means it never sees the Python backend.
Railway's `Root Directory: backend` setting means it never sees the Node.js frontend.
