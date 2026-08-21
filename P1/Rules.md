# Rules.md

Boundaries and conventions the AI (and contributors) must follow while building this project.

## General Principles
- Follow the structure defined in `Architecture.md` — do not invent new top-level folders without updating that file first.
- Build in the order defined in `Phases.md`. Do not jump ahead to later-phase features while a current phase is incomplete.
- Before starting a coding session, read `Memory.md` to recover context. Update `Memory.md` at the end of every session/phase.
- Keep controllers thin: no direct SQLAlchemy queries in `controller/`. All DB access goes through `dao/`.
- Keep business logic (validation, score calculation, permission logic) in `service/`, not in controllers or models.

## Allowed Libraries
- Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-JWT-Extended (or PyJWT), Werkzeug (password hashing), python-dotenv, Pytest, PyMySQL or mysqlclient (MySQL driver).
- Standard library modules as needed (os, datetime, uuid, etc.).

## Disallowed / Avoid
- Do not use raw string-concatenated SQL — always use SQLAlchemy ORM/queries to avoid SQL injection.
- Do not store plaintext passwords — always hash with Werkzeug or bcrypt.
- Do not commit `.env`, `myvenv/`, `uploads/`, `__pycache__/`, or any secrets — must be listed in `.gitignore`.
- Do not use Flask's built-in dev server config for production (`debug=True` only in local/dev config).
- Do not hardcode file paths, secrets, or DB credentials — use environment variables via `config/config.py`.
- Do not skip input validation on any form or API endpoint.
- Avoid deeply nested conditional logic in controllers — extract to service functions.

## File Upload Rules
- Only accept extensions explicitly listed in `ALLOWED_EXTENSIONS` (PDF, PNG, JPG, JPEG, MP4, DOC, DOCX).
- Enforce a max file size (e.g., 50MB) — reject larger uploads with a clear error.
- Always use `secure_filename()` (or equivalent) before saving to disk.
- Never trust the client-provided MIME type alone — validate extension and, where feasible, file signature.

## Error Handling
- All API endpoints must return consistent JSON error responses: `{"error": "<message>"}` with an appropriate HTTP status code (400, 401, 403, 404, 500).
- Never expose raw stack traces or internal exception messages to the client in production.
- Log unexpected errors server-side (structured logging preferred).
- Every DB write operation must be wrapped so failures roll back the transaction cleanly.

## Authorization Rules
- Every protected route must explicitly declare which role(s) can access it.
- Default-deny: if a route's role requirement isn't specified, treat it as forbidden rather than open.
- Students must never be able to access another student's data (progress, quiz results, enrollment) directly via ID manipulation — always check ownership server-side.

## Testing Rules
- Every new feature/endpoint must ship with at least one corresponding test in `tests/`.
- Tests must cover both the happy path and at least one failure/edge case (invalid input, unauthorized access).
- Do not mark a phase "done" in `Memory.md` until its tests pass.

## Coding Style
- Follow PEP 8 for Python code.
- Use descriptive names for routes, functions, and variables — avoid single-letter names outside of loop counters.
- Keep functions focused (single responsibility); prefer several small functions over one large one.
- Comment non-obvious business logic (e.g., score calculation edge cases), not obvious code.

## AI-Specific Working Rules
- Do not regenerate or rewrite entire files when a small, targeted edit will do.
- Do not fabricate database columns, routes, or behavior not defined in `PRD.md` or `Architecture.md` — ask/flag if something is ambiguous.
- When context is limited, rely on `Memory.md` and file structure rather than re-reading the entire codebase.
- If a requested change conflicts with `Rules.md` or `Architecture.md`, flag the conflict instead of silently overriding it.
