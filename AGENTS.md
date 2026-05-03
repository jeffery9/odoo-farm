# 🤖 AI Agents & Developer Guidelines

This document defines the operational rules for AI agents and developers working on the Odoo Farm Management System (Odoo 19).


## 0. Quick Navigation
*   **[LLM START HERE](docs/LLM_START_HERE.md)**: The Master Entry Point. Contains core Doc-Driven development paradigms, absolute mandates, and bilingual policy. You MUST align with this document before any logic implementation.

## 1. Branching Strategy & Release Flow

*   **Development (`dev`)**: All new features, bug fixes, and experiments MUST be performed on the `dev` branch.
*   **Release (`19.0`)**: The `19.0` branch is reserved for stable, production-ready code.
    *   Releases are moved from `dev` to `19.0`.
    *   **CRITICAL**: Only code-related commits are allowed on the `19.0` branch.

## 2. Commit & Separation Standards

*   **Atomic Commits**: Keep changes small and focused.
*   **Decoupled Documentation**: Documentation updates (Markdown files, technical docs) and Code changes (Python, XML, JS) MUST be in **separate commits**.
    *   Example: Do not mix a `README.md` fix with a Python model change in the same commit.
*   **Release Filtering**: During the release process to the `19.0` branch, agents/developers must ensure that documentation-only commits are filtered out or handled separately. The `19.0` branch should remain a pure code-executable baseline.

## 3. Technical Mandates (Odoo 19)

*   **De-industrialization**: Always prioritize agricultural semantics (e.g., "Missions" instead of "Work Orders").
*   **ISL Architecture**: Strictly follow the Industry Specialized Layer (ISL) patterns using `_inherits`. Use the `Redirector` for UI flow.
*   **Test-Driven Development (TDD)**: Aim for 100% reliability. New features must include automated smoke tests or unit tests.
*   **Odoo 19 Syntax**:
    *   Use `list` instead of `tree` in XML.
    *   Use `invisible`, `readonly`, `required` attributes instead of the legacy `attrs` dictionary.
    *   Always define `ondelete` policies for `selection_add` fields.

## 4. Maintenance & Cleanup

*   Regularly clean up temporary migration scripts (e.g., `fix_*.py`).
*   Ensure all module manifests (`__manifest__.py`) are valid Python dictionaries and pass `ast.literal_eval`.
