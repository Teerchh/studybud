# StudyBuddy — Tailwind CSS Migration & Fixes

> Progress tracker for migrating the project to Tailwind CSS, fixing responsiveness,
> and resolving the stale Vercel deployment (green page).

> **Approach note:** We preserve the existing StudyBuddy design by importing the
> original `static/css/style.css` into the Tailwind build (`tailwind/input.css`),
> rather than hand-converting every template to utility classes. This keeps the
> exact look while giving us Tailwind's build pipeline + utilities for responsive fixes.

## 0. Baseline / Context

- [x] Diagnosed green page: live Vercel build serves stale `main.css` with `body { background-color: aquamarine; }`
- [x] Confirmed current `main` code is dark-themed and already pushed (`main` == `origin/main`)
- [x] Confirmed root cause is a stale deployment, not code
- [x] Agreed approach: Tailwind CLI (production-grade)

---

## 1. Tailwind Build Pipeline (Node / pnpm)

- [x] Create `package.json` (Tailwind v4 + `@tailwindcss/cli`, `packageManager: pnpm`)
- [x] Create Tailwind input CSS (`tailwind/input.css`) with `@import "tailwindcss"` + `@source`
- [x] Define StudyBuddy color palette in `@theme`
  - [x] `--color-main: #71c6dd` (light blue/teal), `--color-main-light: #e1f6fb`
  - [x] `--color-dark: #3f4156`, `--color-dark-medium: #51546e`, `--color-dark-light: #696d97`
  - [x] `--color-bg: #2d2d39`, `--color-light: #e5e5e5`, `--color-gray: #8b8b8b`
  - [x] `--color-success: #5dd693`, `--color-error: #fc4b0b`
- [x] Import existing `static/css/style.css` into the Tailwind build (preserve design)
- [x] Add scripts: `build`, `watch`
- [x] Install with `pnpm install` and verify `pnpm run build` compiles `static/css/tailwind.css`
- [x] Add `node_modules/` to `.gitignore` (compiled `static/css/tailwind.css` is now COMMITTED so whitenoise can serve it — see § 7)
- [x] Delete `package-lock.json` (npm artifact); commit `pnpm-lock.yaml`
- [x] Update `vercel.json` buildCommand (originally pnpm chain; later simplified to `python manage.py collectstatic --noinput` for the deploy fix — see § 7)

---

## 2. Django Settings & Static Setup

- [x] `STATICFILES_DIRS` already includes `static/`; added `WHITENOISE_USE_FINDERS = True` (deploy fix, § 7)
- [x] `STATIC_ROOT` + whitenoise already configured for Vercel
- [x] Verified `collectstatic --dry-run` picks up `static/css/tailwind.css`

---

## 3. Base Layout & Navbar

- [x] `templates/layout.html` — links `tailwind.css` + Google Fonts, dark body, fixed messages
- [x] `templates/navbar.html` — restored to original design (styled via imported `style.css`)
- [x] Reverted `static/js/script.js` dropdown toggle to original `.show` behavior
- [x] Confirmed navbar renders with correct dark theme (no green)

---

## 4. Page Templates & Components

> Preserved via the imported `style.css` (no per-template utility rewrite needed).

- [x] `base/templates/base/home.html` renders correctly (3-column layout)
- [x] `base/templates/base/room.html` renders correctly
- [x] `base/templates/base/profile.html` renders correctly
- [x] `base/templates/base/topics.html` renders correctly
- [x] `base/templates/base/activity.html` renders correctly
- [x] `base/templates/base/create_room.html` renders correctly
- [x] `base/templates/base/edit_user.html` renders correctly
- [x] `base/templates/base/delete.html` renders correctly
- [x] `base/templates/base/login_register.html` renders correctly
- [x] Components: `feed_component`, `topics_component`, `activity_component` render correctly

---

## 5. Responsiveness

- [x] Home: collapse 3-column layout to single column on mobile
- [x] Navbar: search/menu behavior on small screens (verified)
- [x] Room page: collapse 2-column layout, hide participants on mobile
- [x] Login/Register: center the auth box; fix signup overflow (flexbox centering in `style.css`)
- [x] Verify across breakpoints (mobile / tablet / desktop) — no horizontal overflow

---

## 6. Cleanup Legacy CSS & Templates

- [x] Stop loading legacy `static/css/main.css` (green source) — already unlinked from `layout.html`
- [x] Remove unused `home_old.html` (confirmed unused, deleted)
- [x] Keep `static/css/style.css` — now the Tailwind input source (`tailwind/input.css` imports it)

---

## 7. Verify & Deploy

- [x] Run Django server locally and check all pages render correctly
- [x] Run `python manage.py collectstatic --noinput` successfully
- [x] Run `python manage.py check` (no issues)
- [x] Confirm compiled CSS has no `aquamarine` (local)
- [x] Decide `assets/` handling — untracked from git (added to `.gitignore`)
- [x] Untrack `.pyc` / `__pycache__` + remove embedded PAT from `origin` remote URL
- [x] Push to `main` via PR (`tailwind-integration` → `main`, merge commit `e8e6a4a` includes `e83d933`)
- [x] Hard-refresh deployed site and confirm green is gone + dark theme applied

### ✅ Deploy issue — RESOLVED

> Live Vercel site had **ALL static files 404** (new HTML served, but unstyled).

- **Cause:** Vercel's `@vercel/python` builder does **not** include `collectstatic` output
  (`assets/`) in the deployed serverless function, and `pnpm` on Vercel silently required
  `ENABLE_EXPERIMENTAL_COREPACK=1` — so the pnpm step aborted before `collectstatic`.
- **Fix (deployed, commit `5d91d2c`, verified):**
  - `WHITENOISE_USE_FINDERS = True` in `settings.py` → whitenoise serves static **directly
    from the committed `static/` folder** at runtime (no `collectstatic`/`assets/` dependency).
  - Committed compiled `static/css/tailwind.css` (single file).
  - Simplified `vercel.json` build command to `python manage.py collectstatic --noinput`.
  - Verified: `/static/*` returns 200, dark theme applied, no green.

---

## 8. Housekeeping / Security

- [x] Remove embedded GitHub PAT from `origin` remote URL (re-added without token: `https://github.com/Teerchh/studybud.git`)
- [ ] Revoke the old GitHub PAT (`ghp_...`) on GitHub → Settings → Developer settings → PATs
- [x] Add `__pycache__/` + `*.py[cod]` to `.gitignore`
- [x] Untrack `assets/`, `.vscode/`, `__pycache__/` from git; `.gitignore` updated for `node_modules/`, `assets/`, `.vscode/` (compiled `tailwind.css` now tracked — § 7)
- [x] `.env*` already gitignored (never commit real secrets)
- [x] Enabled Git Credential Manager

---

## 9. CI/CD (GitHub Actions + Docker)

- [x] Created `Dockerfile` (multi-stage: Tailwind CSS → Python app → runtime) — build verified, `manage.py check` passes
- [x] Created `.github/workflows/deploy.yml` (Docker build + checks; deploy to Vercel on push to `main`)
- [x] Created `.dockerignore` + `.vercelignore`
- [ ] Add GitHub repository secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
- [ ] Note: after CSS changes, commit the compiled `static/css/tailwind.css` (whitenoise serves it from `static/`)
- [x] `.vscode/settings.json` — file no longer present on disk (was untracked); nothing to confirm
