# 🤖 Agent Instructions (Google Antigravity)

## 🏗️ Phase 1: Planning (Discovery)
Before writing any code, initializing files, or installing dependencies, you must complete the following:
1.  **Clarification:** Ask 5-7 targeted questions to refine the app's features, user flow, and technical constraints.
2.  **Issue Check:** explicitly ask the user: *"Would you like to address any open GitHub issues during this session?"* list the top 3-5 open issues if possible.
2.  **Tech Stack Selection:** Propose a tech stack based on our discussion.
3.  **Architecture:** Generate a **Technical Design Artifact**. This must include:
    * System architecture overview.
    * Database schema/Data models.
    * Step-by-step implementation roadmap.
4.  **Halt:** Do not proceed to Phase 2 (Coding) until the Technical Design Artifact is explicitly approved by the human user.

## 🌿 Git & Branching Protocol (Strict)
1.  **Working Branch:** You are prohibited from working on the `main` branch. 
2.  **Setup:** Immediately check if a branch named `agy` exists. If not, create it.
3.  **Context:** Treat `agy` as the "Main" branch for all your agentic operations. 
4.  **Sub-branching:** You may create feature-specific branches (e.g., `agy/feat-login`) derived from `agy`, but they must be merged back into `agy`.
5.  **Commits:** Make atomic commits to the `agy` branch for every task completed (e.g., "Added Auth schema").
## 🐛 GitHub Issues Protocol
1.  **Source:** Monitor `https://github.com/ganeshbmc/med-brief/issues` for bug reports and feature requests.
2.  **Branching:**
    *   Create a dedicated branch from `agy` for the issue (e.g., `agy/issue-12-fix-login`).
    *   **NEVER** work on `main`.
3.  **Workflow:**
    *   Read the issue details.
    *   Reproduce the issue locally if possible.
    *   Implement the fix on the `agy`-derived branch.
    *   Verify the fix.
    *   Merge back to `agy` (or keep on the feature branch if requested).

## 🛠️ Execution Rules
> [!IMPORTANT]
> **WSL MANDATE:** The host CLI is PowerShell, but the dev environment is Linux.
> **RULE:** Every terminal command MUST be prefixed with `wsl` (e.g., `wsl git status`, `wsl npm run dev`). **Failure to do so is a protocol violation.**

*   **Environment:** Windows Host → WSL Execution.
*   **Path Handling:**
    *   **Terminal:** Use Linux paths (e.g., `/mnt/d/Github/...`).
    *   **File Editing:** Use Windows paths (IDE handles translation).
*   **Git:** Always use `wsl git ...` on the `agy` branch.
*   **Validation:** Verify functionality in browser before claiming success.
*   **No Sprawl:** Modular code only.

## 🛑 Boundaries
* **Do Not** touch the `main` branch.
* **Do Not** push to a remote repository without confirmation if credentials are not pre-configured.
* **Do Not** delete existing project documentation unless specifically requested.

## 📝 Documentation & Artifact Backup
**CRITICAL:** To prevent data loss during agent crashes:
1.  Every time you update `implementation_plan.md` or `task.md` (or any other artifact) in the official memory, you **MUST** immediately save a separate copy to the `.antigravity/history/` directory.
2.  Use the same filename (e.g., `.antigravity/history/implementation_plan.md`). Overwrite existing files to ensure the history folder always has the latest version.