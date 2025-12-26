# 🤖 Agent Instructions (Google Antigravity)

## 🏗️ Phase 1: Planning (Discovery)
Before writing any code, initializing files, or installing dependencies, you must complete the following:
1.  **Clarification:** Ask 5-7 targeted questions to refine the app's features, user flow, and technical constraints.
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

## 🛠️ Execution Rules
* **Terminal Policy:** Use the Ubuntu (WSL2) terminal for all commands.
* **Validation:** After writing code, use the integrated browser or test suites to verify functionality before reporting a task as complete.
* **No Sprawl:** Keep code modular. Favor small, specific files over large "god files."

## 🛑 Boundaries
* **Do Not** touch the `main` branch.
* **Do Not** push to a remote repository without confirmation if credentials are not pre-configured.
* **Do Not** delete existing project documentation unless specifically requested.
