# AGENTS.md

## Cursor Cloud specific instructions

This is a single **Django 4.2** project (`mysite`) that serves three apps under one dev server:
`blog` (`/blog/`), `polls` (`/polls/`), and `user_manager` (`/user/`, `/contact/`), plus Django
admin (`/admin/`) and allauth social login (`/accounts/`). There is no separate frontend build
and no external services are required — the default database is SQLite and static files are served
in-process by WhiteNoise.

### Environment

- Python dependencies live in a virtualenv at `.venv/` (gitignored). Activate with
  `source .venv/bin/activate`, or call binaries directly via `.venv/bin/python`.
- The startup update script keeps `.venv` in sync with `requirements.txt`. It does NOT run
  database migrations (see below).

### Running the app (dev)

- Standard commands are documented in `README.md`. In short, after activating the venv:
  - `python manage.py migrate` — required on a fresh VM because `db.sqlite3` is gitignored and
    NOT part of the repo/snapshot, so the database must be (re)created before the server will work.
  - `python manage.py runserver 0.0.0.0:8000` — dev server.
- There is no admin user by default. Create one for testing the admin / login-gated flows, e.g.
  `DJANGO_SUPERUSER_PASSWORD=admin12345 python manage.py createsuperuser --username admin --email admin@example.com --noinput`.

### Lint / test / build

- Lint / system check: `python manage.py check`
- Tests: `python manage.py test polls mysite blog user_manager` (README lists `polls mysite`;
  `blog` and `user_manager` also have tests).
- No build step is required (WhiteNoise serves static files; `collectstatic` is only needed for
  prod-style serving).

### Gotchas

- `python` may not be on PATH outside the venv; use `python3` or the activated venv's `python`.
- Optional integrations are off by default and need no setup for core flows: PostgreSQL
  (`USE_POSTGRES=1` / `DATABASE_URL`), SMTP email (password reset), and OAuth providers
  (Google/Facebook/Instagram via allauth).
- `django-debug-toolbar` only loads when `DEBUG=True` and not running tests.
