# Agent instructions

## Workflow
- Work in small, self-contained PRs. The user commits and opens PRs.
- Always create a new branch before making changes for a step. Never work on `main`.
- After each step, explain how to run and validate it, and wait for approval before the next step.
- Ask when the spec is unclear. Do not assume.

## Code
- Minimal changes and as few files as possible. Pick the simplest solution.
- Follow clean code and best practices for Python, Next.js and React. This is a PoC, so do not overengineer.
- Comments in English, only when the "why" is not obvious.
- Keep README and docs as concise as possible.

## Repo
- The 100-property stratified sample is committed for reproducibility. Running the pipeline again overwrites it.
- Pipeline execution stays as simple as possible: `uv run pipeline run-all`.
