---
name: markdown2docx
description: Convert a canonical MySDD Markdown document under openspec/publics to a same-name DOCX with Pandoc. Do not use this skill to author content.
---

# Convert Markdown to DOCX

Accept one Markdown path under `openspec/publics/`. The output MUST be the
same directory and basename with the `.docx` extension. Use
`openspec/publics/reference.docx` as the reference document.

## Validate

Resolve all paths literally from the repository root. Stop before rendering
when the input or reference document is missing, the input is outside
`openspec/publics/`, or the output contract is not satisfied. Record the
input SHA-256 hash before conversion.

## Convert

<!-- markdownlint-disable MD013 -->

```powershell
# Run the pinned Pandoc through mise and apply the shared reference document.
mise exec pandoc@3.11 --command "pandoc '<input.md>' --from=gfm --to=docx --reference-doc='openspec/publics/reference.docx' --output='<same-basename.docx>'"
```

<!-- markdownlint-enable MD013 -->

## Verify and report

Confirm that Pandoc exited successfully, the DOCX exists and is non-empty,
and the input SHA-256 hash is unchanged. Return the absolute DOCX path on
success. On any failure, keep the source Markdown and report partial success
to the caller; never report a usable DOCX without all checks passing.
