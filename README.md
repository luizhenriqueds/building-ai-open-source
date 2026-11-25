# building-ai-open-source

BidRank: an AI real-estate search demo built with open-source tools.

## Setup

```bash
uv tool install pre-commit
pre-commit install
```

The crawl stage needs a browser once: `cd batch-pipelines && uv run crawl4ai-setup`.

## Run the app

```bash
cd batch-pipelines && uv run uvicorn api.main:app --reload   # API on :8000
cd frontend && npm install && npm run dev                    # UI on :3000
```
