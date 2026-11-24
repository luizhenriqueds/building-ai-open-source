# Agent instructions

## Workflow
- Work in small, self-contained PRs. The user commits and opens PRs.
- Always create a new branch before making changes for a step. Never work on `main`.
- After each step, explain how to run and validate it, and wait for approval before the next step.
- Ask when the spec is unclear. Do not assume.

## Code
- Minimal changes and as few files as possible. Pick the simplest solution.
- Follow clean code and best practices for Python, Next.js and React. This is a PoC, so do not overengineer.
- Comments in English, only when the "why" is not obvious. No header comments at the top of Python files.
- Keep README and docs as concise as possible.
- Python: keep constants out of the logic modules. Shared settings live in `pipeline/config.py`; stage-specific constants get their own `pipeline/<stage>_config.py` (e.g. `crawl_config.py`) when they grow.
- Python: use the `logging` module (`logger = logging.getLogger(__name__)`), never `print`.
- Use meaningful, descriptive names. No short or meaningless names (`a1`, `rng`, `p`, `k`).
- Keep functions short and flat. Split long functions and avoid nested levels.
- Every function gets a docstring: one summary line plus a brief `Args:` section.

## Repo
- The 100-property stratified sample is committed for reproducibility. Running the pipeline again overwrites it.
- Pipeline execution stays as simple as possible: `uv run pipeline run-all`.
