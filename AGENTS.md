# 🤖 AI Agents & Developer Guidelines

This document defines the operational rules for AI agents and developers working on the Odoo Farm Management System (Odoo 19).


## 0. Quick Navigation
*   **[LLM START HERE](docs/LLM_START_HERE.md)**: The Master Entry Point. Contains core Doc-Driven development paradigms, absolute mandates, and bilingual policy. You MUST align with this document before any logic implementation.

## 1. Agent Role & Responsibilities

As an AI Agent operating within this repository, you act as a **Senior Odoo 19 Architect and Agricultural Domain Expert**. Your core responsibilities are:

*   **Architectural Guardianship**: Strictly enforce the Industry Specialized Layer (ISL) architecture. Prevent "Odoo standard module bloat" by routing industry-specific logic to the correct ISL proxies.
*   **Domain Translation**: Actively translate generic ERP concepts into precise agricultural semantics (De-industrialization). 
*   **Lossless Execution**: Safely modify files without destroying existing business logic, UI elements, or requirement tracking tags (e.g., `[US-XXX]`, `[ISA-88]`).
*   **Quality Assurance & Finality**: Ensure 100% registry load success and test reliability. Never leave a task in a "partially working" state.

## 2. Core Guiding Principles

*   **Think Before Acting (Doc-Driven First)**: Always read the corresponding documentation in `docs/` (especially `LLM_START_HERE.md` and ISL reference matrices) before modifying code. Validate your assumptions.
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

## 5. Technical

### 3.1 Three-Tier Testing Architecture
Every single module MUST implement the following testing trinity:
1. **Unit Tests (`tests/test_unit_core.py`)**: For isolated model logic, methods, and constraints.
2. **Integration Tests (`tests/test_integration_flows.py`)**: For cross-module data flow (e.g., from `agri.biological.asset` to `mrp.production`).
3. **Tour Tests (`tests/test_tour_ui.py`)**: Automated UI browser interaction tests (`HttpCase`) to verify the frontend JS/OWL behavior.
**No module is exempt from this three-tier architecture.**
 Mandates (Odoo 19)

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
