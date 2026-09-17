---
name: generate-hld
description: Generate or regenerate the MySDD high-level design document in Markdown and DOCX from one OpenSpec change.
---

# Generate HLD

Accept exactly one `change-name`.

## Read

- `openspec/changes/<change-name>/proposal.md`
- One or more `openspec/changes/<change-name>/specs/**/spec.md`
- `openspec/changes/<change-name>/design.md` when it exists
- [HLD template](assets/hld.md)

Stop if the proposal or every Delta Spec is missing. Preserve capability
paths, requirement headings, scenario names, design headings, IDs, and their
traceability. Never invent a design fact; write `TBD` when design input is
absent or incomplete.

## Write

Render the template to `openspec/publics/hld.md`. Map requirements and quality
targets to design decisions and verification evidence. Do not create an
OpenSpec artifact or modify the source change.

After the Markdown is complete, read
[markdown2docx](../markdown2docx/SKILL.md) and delegate conversion of
`openspec/publics/hld.md` to `openspec/publics/hld.docx`.

## Report

Success requires a complete HLD Markdown file with preserved traceability and
a non-empty DOCX. If DOCX conversion fails, keep the Markdown and report
partial success with the conversion failure.
