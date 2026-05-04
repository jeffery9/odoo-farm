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
- **Total Epic Audit**: The backlog has evolved to a strict 001-129 sequential structure. Always refer to `Epic_Number_Mapping.md` and `EPICS_AND_USER_STORIES.md` before generating new requirements.
- **Acceptance Criteria (AC)**: ALL User Stories must have a strict BDD-style Acceptance Criteria block. Code tests MUST implement Assertions mapped back to these ACs using `test_ac_xx_name` conventions.
- **US Tagging**: In the codebase (XML, Python, Models, Tests), refer to stories using the new `[US-XXX-YY]` standard where XXX is the 3-digit Epic number. Do NOT use legacy 1-or-2 digit variants.
