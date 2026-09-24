# EduVerse source structure audit notes

Scope: the 15 TeX source files transitively included by `main.tex`, plus `references.bib`. Unused diagram templates were excluded from the active-document inventory.

## Inventory and source/index correspondence

- 8 numbered chapters, 51 numbered sections, and 28 numbered subsections: 87 numbered TOC entries. All names, numbers, and order match the current source.
- 7 intentionally indexed unnumbered headings: Abstract, Acknowledgements, Contents, List of Figures, List of Tables, Conclusion, References. Total TOC entries: 94.
- 48 starred subordinate headings are intentionally unnumbered and do not issue `addcontentsline`; their absence from the TOC is consistent with the source.
- Chapter-opening items exactly match every chapter's main sections, with no missing, duplicate, reordered, or obsolete item: Chapter 1: 6; Chapter 2: 6; Chapter 3: 4; Chapter 4: 8; Chapter 5: 4; Chapter 6: 14; Chapter 7: 5; Chapter 8: 4. Total: 51.
- The chapter-opening macro obtains title, number, and page from `nameref`, `ref*`, and `pageref*` (main.tex:107–118), so it contains no independently maintained title or page text.
- 52 figure captions and 38 table captions match their LOF/LOT records in source order. The 33 generated physical-schema table captions are expanded from `EduSchemaTableStart`.
- Initial inventory: 139 unique labels, 78 distinct referenced targets (51 chapter-opening targets plus 27 ordinary figure/table references), 23 citation-key uses representing all 14 bibliography entries. No missing or duplicate label/reference/citation key.
- The 25 screenshot labels' auxiliary `nameref` titles omit their captions' final full stop, which is normal `nameref` title handling. Their printed captions and LOF captions retain the full stop and match.
- Three literal numeric references are correct: Chapter 5 at chapter6_implementation.tex:20 and :148; Chapter 3 at :288.

## Chapter 3 structure and paragraph integrity

The source exactly matches the requested structure and all four requested opening labels:

| Source line | Number | Heading | Label |
|---|---|---|---|
| 8 | 3.1 | Introduction | sec:methodology_introduction |
| 20 | 3.2 | Methodological Approach | sec:system_development_methodology |
| 23 | 3.2.1 | Iterative Feature-Centered Development | subsec:feature_based_iterative_workflow |
| 40 | 3.2.2 | Vertical-Slice Realization | subsec:vertical_slice_development_approach |
| 58 | 3.2.3 | Why This Methodology Fits EduVerse | subsec:justification_for_methodology_selection |
| 76 | 3.3 | Repeated Development Cycle | sec:development_workflow_structure |
| 118 | 3.4 | Chapter Summary | sec:chapter3_summary |

Table 3.1's caption is at line 93, followed immediately by its label at line 94; both are inside the table environment in section 3.3. The version-control paragraph follows the table environment and precedes section 3.4. Its position is intentional in the source.

The pre-audit Git working-tree diff for Chapter 3 contained one newly added sentence in section 3.2 about initial requirements, plus removal of the empty line before 3.2.1. No paragraph, heading, table, or table row was deleted or reordered. The missing empty line before `subsection` is harmless because the heading command ends the preceding paragraph. A normalized duplicate check of 197 substantial prose paragraphs across the thesis found no exact duplicate paragraph.

## Genuine source build defect

`chapters/chapter5_system_design.tex:296` originally contained:

```tex
\label{*subsec\:database\_tables*}
```

The root audit's clean build confirmed this caused `Missing \endcsname inserted` while rereading the generated Chapter 5 auxiliary file. It was the only active label key containing characters outside letters, digits, colon, underscore, period, and hyphen. No reference used that key.

Root applied the minimal replacement:

```tex
\label{subsec:database_tables}
```

This changes no visible text or layout and attaches the label to the same subsection 5.3.4.

## Minor latent label caveat

`backmatter/conclusion.tex:1` defines `chap:conclusion` immediately after unnumbered `chapter*`. Its title, page, and hyperlink destination are correct; its numeric auxiliary field inherits 8.4 from the last numbered section. No source command references this label. Thus there is no displayed wrong conclusion reference. Removing the unused label is the smallest optional remedy if the raw numeric metadata must also be clean; no heading/counter redesign is warranted.

## Float source context for visual audit

- Chapter 4 lines 309–673 locally replace figure floats with indivisible minipages. The descriptions intentionally precede two grouped diagram sequences. Clear pages at 440, 507, 619, and 675 establish their ordering and keep the diagrams in their intended sections.
- Chapter 5 flushes the ERD before the next subsection and flushes each screenshot group before the next interface subsection.
- Chapter 6's table is introduced in section 6.2, followed by a `FloatBarrier` at line 68. `main.tex:26` defines that barrier as a no-op. The initial auxiliary records place section 6.3 on page 109 and the table on page 110. This is ordinary deferred-float behavior but needs a visual judgment against the user's request to identify misplaced floats. The root audit handles actual rendered-page verification.

The final source/auxiliary/index inventory is reproducible with `audit_source.py`; `source-audit.json` contains the full per-entry evidence. Rerun it after the root build stabilizes to refresh page metadata.
