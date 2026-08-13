# StudyBuddy

> Find study partners around the world! A Django-based study-room community app where users
> create topic-based rooms, chat, and connect with other learners.

## ✨ Features

- **Rooms** — create, update, and delete study rooms by topic
- **Chat threads** — post and reply inside each room
- **Profiles** — avatars, bios, and a list of hosted rooms
- **Topics & search** — browse topics and search rooms by keyword
- **Recent activities** — live feed of the latest messages
- **Responsive UI** — dark theme, mobile-friendly layouts (Tailwind CSS)

## 🧰 Tech Stack

| Layer | Tech |
|---|---|
| Backend | Django 6, Django REST Framework |
| Database | PostgreSQL (Neon) — falls back to SQLite locally |
| Frontend styling | Tailwind CSS v4 (compiled with pnpm) |
| Static files | WhiteNoise (`WHITENOISE_USE_FINDERS` — serves from `static/`) |
| Deployment | Vercel (`@vercel/python`) |
| CI/CD | GitHub Actions + Docker (build/checks → Vercel deploy) |

## �️ Neon Database (production)

StudyBuddy uses [Neon](https://neon.tech) — serverless PostgreSQL — in production.

### 1. Create a Neon project
1. Sign up at https://neon.tech and create a new project.
2. Copy the **connection string** (looks like this):
   ```
   postgresql://user:password@ep-xxxx-xxxx-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
   > Use the **pooled** connection string (the `-pooler` host) for serverless apps.

### 2. Wire it up

- **Local development** — **nothing to do.** Without a `DATABASE_URL`, Django uses the local
  SQLite file (`db.sqlite3`) automatically. You do **not** need the Neon URL locally.
- **Production (Vercel)** — add the Neon URL as an environment variable in the project:
  - Vercel → your project → **Settings → Environments** → add `DATABASE_URL` (Production).
- **CI/CD** — if your workflow needs the DB (e.g., running migrations/tests in CI), also add
  `DATABASE_URL` as a GitHub Actions secret.

### 3. Run migrations against it
```bash
python manage.py migrate
```

> If `DATABASE_URL` is unset, Django automatically falls back to the local SQLite file
> (`db.sqlite3`) — handy for quick local development without a remote DB.

---

## �🚀 Getting Started (local development)

### Prerequisites
- Python 3.14+ (on macOS/Linux the command is usually `python3`)
- Node.js 24+ and [pnpm](https://pnpm.io/installation)
- [Docker](https://www.docker.com/) (optional — only needed for the Docker build)

### 1. Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux (bash/zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
pnpm install
```

### 3. Set up environment
Create `.env.local` (already gitignored) — or export the same vars in your shell:
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Optional: point at a real DB. If omitted, SQLite (db.sqlite3) is used.
# DATABASE_URL=postgresql://user:pass@host:5432/db
```

### 4. Migrate + run the dev server
```bash
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/

> **Tip:** on macOS/Linux, if `python` isn't found, use `python3` instead.

### Tailwind (during development)
Run in a separate terminal so CSS auto-rebuilds on changes:
```bash
pnpm run watch
```
> 🛈 The compiled `static/css/tailwind.css` is **not committed** — it's built automatically
> during the CI/CD deploy (`pnpm run build`) and uploaded with the deployment. No manual
> commit needed.

## 🐳 Docker

A multi-stage `Dockerfile` builds the app (Tailwind CSS → Python app → runtime):

```bash
docker build --target app -t studybud:ci .
docker run --rm studybud:ci python manage.py check
```

## ☁️ Deployment

- **Vercel** (`vercel.json`) — `@vercel/python` + `collectstatic`. Static files are served
  from the `static/` folder via WhiteNoise (`WHITENOISE_USE_FINDERS = True`).
- **CI/CD** (`.github/workflows/deploy.yml`) — on every push to `main`:
  1. Docker build + `manage.py check`
  2. If checks pass → deploy to Vercel (`vercel --prod`)
- Vercel's auto-build is **disabled** via an *Ignored Build Step* (exit 0) so the CI is the
  sole deployer and issues are caught before going live.

> Requires GitHub repo secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.

## 📁 Project Structure

```
studybud/
├── base/                 # main app (models, views, templates, API)
│   ├── api/              # DRF serializers + views
│   ├── templates/base/   # page templates
│   └── models.py         # User, Topic, Room, Message
├── studybud/             # project config (settings, urls, wsgi)
├── static/               # source static assets (CSS, images, JS)
│   └── css/tailwind.css  # compiled Tailwind output (built during deploy, not committed)
├── tailwind/input.css    # Tailwind v4 input + theme palette
├── templates/            # base layout + navbar
├── .github/workflows/    # CI/CD pipeline
├── Dockerfile
├── vercel.json
└── requirements.txt
```

## 🔐 Notes

- `assets/` (collectstatic output) and `.env.local` are gitignored — never commit secrets.
- User-uploaded files live in `assets/images/` (local only); Vercel's serverless filesystem
  is ephemeral, so for persistent uploads in production, add external storage (S3/Cloudinary).
