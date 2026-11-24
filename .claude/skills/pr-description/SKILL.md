---
name: pr-description
description: Write a PR description for the current branch following .github/PULL_REQUEST_TEMPLATE.md. Use when asked for a PR description or PR text.
---

1. Read `.github/PULL_REQUEST_TEMPLATE.md` and keep its sections, order and headings exactly.
2. Run `git diff main...HEAD --stat` and `git log main..HEAD --oneline`, then read the diff.
3. Fill the sections:
   - **Describe your changes**: 2-4 one-line bullets, no file lists or implementation detail.
   - **Issue ticket number and link**: the ticket if known, otherwise `N/A`.
   - **How you tested the code**: the exact commands to validate, with the expected result.
   - **Checklist**: tick only items that are true for this PR.
4. Output the description as markdown for the user to paste. Do not create the PR or commit anything.
5. End the description with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
