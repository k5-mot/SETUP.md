---
name: generate-prd
description: Generate or regenerate the MySDD product requirements document in Markdown and DOCX from one OpenSpec change.
---

# Generate PRD

Accept exactly one `change-name`.

## Read

- `openspec/changes/<change-name>/proposal.md`
- One or more `openspec/changes/<change-name>/specs/**/spec.md`
- [PRD template](assets/prd.md)

Stop if the proposal or every Delta Spec is missing. Preserve capability
paths, requirement headings, scenario names, IDs, and their traceability.
Never turn an unstated fact into a requirement; write `TBD` for missing input.

## Write

Render the template to `openspec/publics/prd.md`. Include each applicable
quality characteristic, measure, target, condition, and verification method.
Do not create an OpenSpec artifact or modify the source change.

After the Markdown is complete, read
[markdown2docx](../markdown2docx/SKILL.md) and delegate conversion of
`openspec/publics/prd.md` to `openspec/publics/prd.docx`.

## Report

Success requires a complete PRD Markdown file with preserved traceability and
a non-empty DOCX. If DOCX conversion fails, keep the Markdown and report
partial success with the conversion failure.
