# 🤖 Directory Execution Policy: Business

> **WARNING**: This directory is governed by both global AI policies and localized domain rules.

## 0. Chain of Command
Before modifying or creating any files in this directory, you **MUST**:
1. Read the global [AGENTS.md](../../AGENTS.md) for Git branching, commit separation, and Odoo 19 mandates.
2. Read the master entry [LLM_START_HERE.md](../../docs/LLM_START_HERE.md) for Doc-Driven development paradigms.

## 1. Localized Domain Rules
- **Domain**: Business Analysis & Epics.
- **Rule**: Focus on the 'What' and 'Why'. Write User Stories in BDD/Gherkin format. Always maintain traceability using `[US-XX-XX]` tags. Do NOT write technical code or database schemas here.

## 2. Documentation Constraints
- **Separation of Concerns**: Code and documentation MUST be committed separately.
- **Lossless Update**: Do not delete or simplify existing architectural anchors, requirement tags (`[US-XXX]`), or tracking IDs.

## 3. Product Governance & Traceability
- **Backlog Structure**: The backlog follows a strict sequential structure (001-137). 
- **Requirement Artifacts**:
    - **Epics (`epics/`目录)**: Markdown documents defining business goals, user stories, and high-level logic.
    - **Features (`features/`目录)**: Gherkin `.feature` files providing the executable BDD specification for each Epic.
- **Traceability Link**: Each Epic has a 1:1 relationship with its Feature file, linked by the 3-digit ID (e.g., `EPIC_001_...md` ↔ `epic_001_...feature`).
- **Acceptance Criteria (AC)**: ALL User Stories must have a strict BDD-style Acceptance Criteria block. Code tests in the `tests/` directory MUST implement Assertions mapped back to these Features.
- **US Tagging**: In the codebase (XML, Python, Models, Tests), refer to stories using the `[US-XXX-YY]` standard. Do NOT use legacy 1-or-2 digit variants.
