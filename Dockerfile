# ---------- Stage 1: Compile Tailwind CSS ----------
FROM node:24-alpine AS css
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY tailwind/ tailwind/
COPY static/css/style.css static/css/style.css
RUN pnpm run build

# ---------- Stage 2: Python app (deps + collected static + checks) ----------
FROM python:3.14-slim AS app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=css /app/static/css/tailwind.css /app/static/css/tailwind.css
COPY . .
RUN python manage.py collectstatic --noinput && \
    python manage.py check

# ---------- Stage 3: Runtime (optional — for `docker run` / container hosting) ----------
FROM python:3.14-slim AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY --from=app /app /app
EXPOSE 8000
CMD ["gunicorn", "studybud.wsgi:application", "--bind", "0.0.0.0:8000"]
