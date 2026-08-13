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
- [x] Add `node_modules/` + compiled `static/css/tailwind.css` to `.gitignore`
- [x] Delete `package-lock.json` (npm artifact); commit `pnpm-lock.yaml`
- [x] Update `vercel.json` buildCommand: `pnpm install --frozen-lockfile && pnpm run build && python manage.py collectstatic --noinput`

---

## 2. Django Settings & Static Setup

- [x] No settings changes needed — `STATICFILES_DIRS` already includes `static/`
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
- [ ] `base/templates/base/room.html`
- [ ] `base/templates/base/profile.html`
- [ ] `base/templates/base/topics.html`
- [ ] `base/templates/base/activity.html`
- [ ] `base/templates/base/create_room.html`
- [ ] `base/templates/base/edit_user.html`
- [ ] `base/templates/base/delete.html`
- [ ] `base/templates/base/login_register.html`
- [ ] Components: `feed_component`, `topics_component`, `activity_component`

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
- [ ] Decide `assets/` handling (committed STATIC_ROOT vs gitignored — see notes)
- [ ] Untrack `.pyc` files + fix `origin` remote URL (remove embedded PAT) before pushing
- [ ] Push to `main` and redeploy on Vercel (or dashboard → Redeploy)
- [ ] Hard-refresh deployed site and confirm green is gone + dark theme applied

---

## 8. Housekeeping / Security

- [ ] Revoke GitHub PAT embedded in `origin` remote URL (GitHub → Settings → Developer settings → PATs)
- [ ] Re-add remote without token: `git remote set-url origin https://github.com/Teerchh/studybud.git`
- [x] Add `__pycache__/` + `*.py[cod]` to `.gitignore`
- [ ] `git rm --cached` the already-tracked `.pyc` files
- [x] `.env*` already gitignored (never commit real secrets)
