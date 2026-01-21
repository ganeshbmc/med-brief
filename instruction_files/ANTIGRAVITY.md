# 🌌 Antigravity Specific Workflow
*Use these instructions ONLY when operating as the Google Antigravity agent.*

## 🏗️ Phase 1: Planning (Discovery)
Before writing any code, initializing files, or installing dependencies, you must complete the following:
1.  **Clarification:** Ask 5-7 targeted questions to refine the app's features, user flow, and technical constraints.
2.  **Issue Check:** explicitly ask the user: *"Would you like to address any open GitHub issues during this session?"* list the top 3-5 open issues if possible.
3.  **Tech Stack Selection:** Propose a tech stack based on our discussion.
4.  **Architecture:** Generate a **Technical Design Artifact**. This must include:
    * System architecture overview.
    * Database schema/Data models.
    * Step-by-step implementation roadmap.
5.  **Halt:** Do not proceed to Phase 2 (Coding) until the Technical Design Artifact is explicitly approved by the human user.

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
*   **Clarification:** If there is any doubt about which CLI tool, IDE, or environment the user is using, **ASK** before proceeding.
