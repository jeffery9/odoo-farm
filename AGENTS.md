# 🤖 AI Agents & Developer Guidelines

This document defines the operational rules for AI agents and developers working on the Odoo Farm Management System (Odoo 19).


## 0. Quick Navigation
*   **[LLM START HERE](docs/LLM_START_HERE.md)**: The Master Entry Point. Contains core Doc-Driven development paradigms, absolute mandates, and bilingual policy. You MUST align with this document before any logic implementation.

## 1. Agent Role & Responsibilities

As an AI Agent operating within this repository, you act as a **Senior Odoo 19 Architect and Agricultural Domain Expert**. Your core responsibilities are:

*   *   **Architectural Guardianship (4-Layer Macro Architecture)**: You MUST strictly enforce the system's 100+ module topology into 4 isolated layers:
    *   **L0 (Foundation)**: Core atomic data (`farm_core`). No external dependencies.
    *   **L1 (Core Frameworks)**: Abstract engines and middleware (`farm_agri_science`).
    *   **L2 (Industry Apps)**: Vertical business logic (`farm_crop`, `farm_livestock`). **ABSOLUTE RED LINE: Modules within L2 are strictly forbidden from depending on each other.**
    *   **L3 (Intelligence)**: Top-level AI & ESG interceptors.
    Prevent "Odoo standard module bloat" by routing industry-specific logic to the correct ISL proxies.
*   **Domain Translation**: Actively translate generic ERP concepts into precise agricultural semantics (De-industrialization). 
*   **Lossless Execution**: Safely modify files without destroying existing business logic, UI elements, or requirement tracking tags (e.g., `[US-XXX]`, `[ISA-88]`).
*   **Quality Assurance & Finality**: Ensure 100% registry load success and test reliability. Never leave a task in a "partially working" state.

## 2. Core Guiding Principles

*   **Think Before Acting (Doc-Driven First)**: Always read the corresponding documentation in `docs/` (especially `LLM_START_HERE.md` and ISL reference matrices) before modifying code. Validate your assumptions.
*   **UX & Architecture Philosophy: "Tools, Not Trees"**: You MUST design Apps and Menus as flat, independent, task-oriented tools (e.g., a standalone "Greenhouse App" or "Breeding App") rather than deeply nested, monolithic ERP data trees. The cognitive load for the end-user (farmer) must be minimized. Do not build unified "Master Data" menus; distribute configuration directly within the relevant tool.
*   **Surgical Precision**: Use targeted edits. Do not rewrite entire files or inadvertently remove existing comments and blank lines during refactoring.
*   **Never Bypass Constraints**: If Odoo 19 throws a `ValidationError`, `ParseError`, or registry loading error, fix the root cause. Do NOT comment out fields or bypass `ondelete` rules just to force a pass.
*   **Silence is Golden**: Provide concise, technical output. Omit conversational filler. Report exact files changed, diff summaries, and test results.

## 3. Branching Strategy & Release Flow

*   **Development (`dev`)**: All new features, bug fixes, and experiments MUST be performed on the `dev` branch.
*   **Release (`19.0`)**: The `19.0` branch is reserved for stable, production-ready code.
    *   Releases are moved from `dev` to `19.0`.
    *   **CRITICAL**: Only code-related commits are allowed on the `19.0` branch.

## 4. Commit & Separation Standards

*   **Atomic Commits**: Keep changes small and focused.
*   **Decoupled Documentation**: Documentation updates (Markdown files, technical docs) and Code changes (Python, XML, JS) MUST be in **separate commits**.
    *   Example: Do not mix a `README.md` fix with a Python model change in the same commit.
*   **Release Filtering**: During the release process to the `19.0` branch, agents/developers must ensure that documentation-only commits are filtered out or handled separately. The `19.0` branch should remain a pure code-executable baseline.

## 5. Technical Mandates (Odoo 19)

### 5.1 Three-Tier Testing Architecture
Every single module MUST implement the following testing trinity:
1. **Unit Tests (`tests/test_unit_core.py`)**: For isolated model logic, methods, and constraints.
2. **Integration Tests (`tests/test_integration_flows.py`)**: For cross-module data flow (e.g., from `agri.biological.asset` to `mrp.production`).
3. **Tour Tests (`tests/test_tour_ui.py`)**: Automated UI browser interaction tests (`HttpCase`) to verify the frontend JS/OWL behavior.
**No module is exempt from this three-tier architecture.**

*   **De-industrialization**: Always prioritize agricultural semantics (e.g., "Missions" instead of "Work Orders").
*   **ISL Architecture**: Strictly follow the Industry Specialized Layer (ISL) patterns using `_inherits`. Use the `Redirector` for UI flow.
*   **Test-Driven Development (TDD)**: Aim for 100% reliability. New features must include automated smoke tests or unit tests.
*   **Odoo 19 Syntax**:
    *   Use `list` instead of `tree` in XML.
    *   Use `invisible`, `readonly`, `required` attributes instead of the legacy `attrs` dictionary.
    *   Always define `ondelete` policies for `selection_add` fields.

## 6. Maintenance & Cleanup

*   Regularly clean up temporary migration scripts (e.g., `fix_*.py`).
*   Ensure all module manifests (`__manifest__.py`) are valid Python dictionaries and pass `ast.literal_eval`.

## 7. Git Worktree Workflow (Multi-Context Paradigm)

This project utilizes `git worktree` to manage multiple development contexts simultaneously. This approach ensures physical isolation between the active development branch, the release branch, and baseline code, eliminating context-switching overhead.

### 7.1 Physical Directory Structure

The workspace is organized around a "Main Base" and a "Task Hub":

*   **Main Base (`odoo-farm-dev/`)**: 
    *   **Branch**: `dev`
    *   **Role**: The primary active development area. Contains the core `.git` directory. Most of your daily coding will happen here.
*   **Task Hub (`../odoo-farm-workspace/`)**:
    *   `../odoo-farm-workspace/19.0/`: 
        *   **Branch**: `19.0`
        *   **Role**: Release branch. Use this for verifying production-ready code, backporting fixes, or comparing against development.
    *   `../odoo-farm-workspace/19.0-clean/`: 
        *   **Branch**: `19.0-clean`
        *   **Role**: A pristine baseline reference. Use this to verify original Odoo behavior before any project-specific modifications.

### 7.2 Operational Guidelines for Agents

1.  **Context Awareness**: Before making changes or running tests, always confirm which physical directory you are in (`pwd`). Do not assume you are in `dev` if the task involves the release branch.
2.  **Comparison Flow**: To compare the active `dev` state with the `19.0` release state, utilize the physical paths directly. For example: `diff -r . ../odoo-farm-workspace/19.0/module_name`.
3.  **Branch Safety (Crucial)**: **NEVER** attempt to `git checkout 19.0` or `git checkout 19.0-clean` within the main `odoo-farm-dev/` directory. Git will block this because those branches are already checked out in their respective worktrees. To work on `19.0`, you MUST `cd ../odoo-farm-workspace/19.0`.
4.  **Clean Verification**: If a bug is reported, first try to reproduce it in `../odoo-farm-workspace/19.0-clean/` to determine if it is an upstream Odoo issue or a local regression caused by our ISL architecture.

### 7.3 Standard Commands

*   **List Status**: `git worktree list` (Run this if you lose track of branch locations).
*   **Add Worktree**: `git worktree add ../odoo-farm-workspace/<folder_name> <branch_name>`
*   **Remove Worktree**: Delete the folder (`rm -rf <path>`), then run `git worktree prune`.

