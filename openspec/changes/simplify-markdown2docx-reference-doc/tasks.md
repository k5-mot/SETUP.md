<!-- markdownlint-disable MD013 MD041 -->

## 1. Reference DOCX and style contract

- [x] 1.1 Inspect the supplied `.agents/skills/markdown2docx/references/template.docx` package and record its page geometry, styles, section references, header/footer parts, and fields as baseline evidence without modifying unrelated package parts.
- [x] 1.2 Normalize the canonical template itself for 10-point body text, `Title`, `TOC Heading`, `Heading 1`, centered tables, intended first/default headers and footers, and `w:updateFields=true`; verify the final OOXML contains each required value and no macros or external relationships (QR-002, QR-004, Security).
- [x] 1.3 Create Japanese `references/style.md` and enumerate fonts, styles, headers, footers, TOC, cover, figure list, and table list with their Pandoc ownership, source prerequisites, field codes, and refresh behavior; compare all eight categories with the final DOCX package (QR-006, maintenance/support).

## 2. Direct Pandoc conversion contract

- [x] 2.1 Update the PRD and HLD authoring assets and maintained public Markdown to use leading YAML title metadata and level-one body chapters; confirm both files parse with `pandoc --from=gfm` and preserve representative IDs (transition).
- [x] 2.2 Rewrite `.agents/skills/markdown2docx/SKILL.md` to validate the YAML title and literal paths, call Pandoc 3.11 directly once with the skill-local `--reference-doc`, `--toc`, `--lof`, and `--lot` options, and retain source-hash, field-refresh, output, and failure-reporting checks (QR-001, QR-004, QR-005).
- [x] 2.3 Update maintained design and workflow documentation to name the skill-local reference DOCX, YAML title contract, direct Pandoc command, and template-owned formatting; verify the repository link checker finds no broken relative links (supply/maintenance).

## 3. Remove duplicated formatting machinery

- [x] 3.1 Replace formatter-based conversion tests with direct Pandoc PRD/HLD tests that assert unchanged source hashes, non-empty outputs, `Title`, representative IDs, TOC/figure-list/table-list fields, field-update settings, page-break styles, centered tables, and repeating table headers (QR-001 through QR-005).
- [x] 3.2 Delete `.agents/skills/markdown2docx/scripts/format_docx.py` and `openspec/publics/template.docx`, then use a full maintained-file search to confirm that the script, old template path, `mise exec pandoc`, and `mise exec python` are no longer referenced (QR-003, disposal).

## 4. Integrated verification

- [x] 4.1 Run the skill-creator validator against `.agents/skills/markdown2docx` and run Markdown lint plus the local-link check; confirm the skill metadata, Japanese style guide, and documentation pass repository rules (QR-003, QR-006).
- [x] 4.2 Run the DOCX conversion regression test and the repository quality suite; confirm PRD and HLD each use one Pandoc process, retain source hashes, and satisfy every structural assertion (QR-001 through QR-005).
- [x] 4.3 Render newly generated PRD and HLD DOCX files with the approved document renderer when available, inspect every page for cover/navigation/body separation, fonts, tables, captions, headers, and footers, and record any unavailable field refresh as deferred to Word rather than reporting cached values as current (QR-002, operation/support).
- [x] 4.4 Run strict OpenSpec validation for `simplify-markdown2docx-reference-doc` and review `git diff --check` plus the final scoped diff; confirm the change is ready for verification and archive without unrelated files.
