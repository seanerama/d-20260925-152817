# Benchmark D

Benchmark fixture D (control app), provisioned 2026-09-25T15:28:17.000Z

> Scaffolded by [Verity](https://github.com/seanerama/verity-framework) — prompt to production, proven.

## Status

See [`STATUS.md`](STATUS.md) for live runtime state (deployed version, environments).

## Project identity

- **slug:** `d-20260925-152817`
- **images:** `ghcr.io/seanerama/d-20260925-152817`

## Run locally

```
pip install -r requirements.txt && flask run
```

Then open http://127.0.0.1:5000/ — the page shows the current server time.

## UI smoke

`pip install -r requirements.txt && flask run` → open http://127.0.0.1:5000/ → the server
time is shown → click **Check health** → live cpu/mem render inline.
