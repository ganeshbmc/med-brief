# 🤖 Agent Instructions

These instructions apply to **all** AI agents (Opencode, Antigravity, etc.) working on this repository.

## 🌿 Git & Branching Protocol (Strict)
1.  **Working Branch:** You are prohibited from working on the `main` branch. 
2.  **Setup:** Immediately check if a branch named `agy` exists. If not, create it.
3.  **Context:** Treat `agy` as the "Main" branch for all your operations. 
4.  **Sub-branching:** You may create feature-specific branches (e.g., `agy/feat-login`) derived from `agy`, but they must be merged back into `agy`.
5.  **Commits:** Make atomic commits to the `agy` branch for every task completed (e.g., "Added Auth schema").

## 🐛 GitHub Issues Protocol
1.  **Source:** Monitor project issues for bug reports and feature requests.
2.  **Branching:**
    *   Create a dedicated branch from `agy` for the issue (e.g., `agy/issue-12-fix-login`).
    *   **NEVER** work on `main`.
3.  **Workflow:**
    *   Read the issue details.
    *   Reproduce the issue locally if possible.
    *   Implement the fix on the `agy`-derived branch.
    *   Verify the fix.
    *   Merge back to `agy`.

## 🔄 Dev Server Restart Protocol
After making code changes, restart the dev servers using:
```bash
bash scripts/restart-dev.sh
```
This script kills existing uvicorn/vite processes and starts fresh backend + frontend servers.

## 🛑 Boundaries
* **Do Not** touch the `main` branch.
* **Do Not** push to a remote repository without confirmation if credentials are not pre-configured.
* **Do Not** delete existing project documentation unless specifically requested.

---

For Google Antigravity specific workflows, see [ANTIGRAVITY.md](./instruction_files/ANTIGRAVITY.md).
