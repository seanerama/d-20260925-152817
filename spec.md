# Repo D — control app spec (benchmark fixture)

**Role in the benchmark:** the tiny, deterministic **control app** (fixture D). Small on
purpose — it's the throwaway that proves the harness loop end-to-end cheaply, and the
low-variance baseline the heavier fixtures (A/C) are read against. Architecture is already
decided here (this is a seed spec, not a design exercise) so the pipeline just builds it.

## What to build

A minimal **Flask** web service:

- **`GET /`** → a single HTML page that shows the **current server time** and a
  **"Check health"** button. The button calls `/health` (fetch) and renders the result
  inline. No framework, no build step on the front end — inline HTML/JS.
- **`GET /health`** → JSON system utilization: `{ "status": "ok", "cpu_percent": <n>,
  "mem_percent": <n>, "time": "<iso>" }`, read via `psutil`. Never throws — a probe error
  degrades to `{ "status": "degraded", "error": "<reason>" }` with HTTP 200 so the page can
  render it honestly.

## Decided choices (no re-litigation)

- **Framework:** Flask (single small dependency). Not FastAPI — no async needed here.
- **Utilization source:** `psutil` (`cpu_percent`, `virtual_memory().percent`).
- **Layout:** `app.py` (the two routes + inline page), `requirements.txt` (`flask`,
  `psutil`), `tests/test_app.py`, `README.md`. Keep it flat and tiny.
- **No auth, no persistence, no external calls.** Bind localhost.

## Acceptance conditions (what the built app must satisfy)

- [ ] `GET /` returns 200 HTML containing the current time and a working "Check health"
      button that calls `/health` and shows the result.
- [ ] `GET /health` returns 200 JSON with `status`, `cpu_percent`, `mem_percent`, `time`;
      a probe failure degrades to `status: "degraded"` (still HTTP 200), never a 500.
- [ ] `tests/test_app.py` (pytest, Flask test client) covers both routes incl. the
      degraded-health path.
- [ ] **UI-smoke:** `pip install -r requirements.txt && flask run` → open `/` → the time
      shows and clicking "Check health" renders live cpu/mem.
- [ ] Hygiene CI green (the scaffolded pipeline).

## Notes for the harness

- This spec is the seed the harness feeds `verity plan` (Mode A) after scaffolding the
  fixture repo. It is intentionally ~3 small stages of work — enough to exercise
  build→review (and a gate, if the variant/policy gates) without meaningful cost.
