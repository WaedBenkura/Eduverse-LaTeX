from pathlib import Path
import json,shutil,hashlib

ROOT=Path(__file__).resolve().parents[2]
AUDIT=Path(__file__).resolve().parent
OUT=ROOT/'docs/structural-pagination-audit-2026-09-23.md'
pdf=json.loads((AUDIT/'pdf-audit.json').read_text(encoding='utf-8'))
source=json.loads((AUDIT/'source-audit/source-audit.json').read_text(encoding='utf-8'))
render=json.loads((AUDIT/'final-visual/render-verification.json').read_text())
passes=json.loads((AUDIT/'build-evidence-staged/passes.json').read_text())
assert not pdf['issues'] and not pdf['reference_warnings']
assert not render['pixel_changed_pages'] and not render['text_changed_pages']
assert passes[-1]['state']==passes[-2]['state']
for field in ('missing_source_labels','missing_aux_labels','duplicate_source_labels','duplicate_aux_labels','unsafe_label_names','undefined_references','undefined_citations','label_attachment_issues'):
    assert not source[field],field

report=r'''# EduVerse thesis: final structural and pagination audit

Audit date: 23 September 2026. Audited output: project-root `main.pdf`.

All page numbers in the findings are **printed thesis page numbers**, unless explicitly identified as physical PDF pages. The document contains one unnumbered cover, front matter **i-xi**, and main matter **1-125**: **137 physical PDF pages**.

## A. Overall Status

**PASS WITH MINOR ISSUES.** After the two minimal label repairs described in section I, all current indexes, chapter-opening contents, captions, labels, references, and actual printed pages are mutually consistent. No unresolved structural indexing or reference defect remains.

The qualification concerns pre-existing presentation details and nonfatal typesetting diagnostics, described in section H. They do not produce missing text, incorrect numbering, stale indexes, or wrong reference destinations. Thesis wording, headings, captions, table content, figures, margins, typography, spacing, and section structure were not changed during this audit. The user's existing Chapter 3 edit was preserved.

The scope is the complete thesis built from `main.tex`, including its 15 active source files, front matter, eight chapters, included diagram sources, Conclusion, and bibliography. Inactive alternative diagram/template files and historical PDFs are not mistaken for content of the current thesis.

## B. Main Table of Contents

**Correct: all 94 entries verified.** These comprise 8 numbered chapters, 51 sections, 28 subsections, and 7 intentionally indexed unnumbered headings: Abstract, Acknowledgements, Contents, List of Figures, List of Tables, Conclusion, and References.

For every entry, source title/number/order were compared with the generated index, the visible PDF index row, the PDF destination, and the actual heading on the destination's printed page. There are no missing expected entries, obsolete entries, duplicate entries, title mismatches, numbering errors, or page mismatches. The 48 starred subsection/subsubsection headings are intentionally unnumbered and unindexed.

Front-matter index starts: Abstract i; Acknowledgements ii; Contents iii; List of Figures vii; List of Tables x. Conclusion starts on 123 and References on 124.

## C. Chapter-Opening Contents

**All 51 entries pass.** Every listed label exists and resolves to the intended section, with the correct title, section number, and printed page. Every chapter lists all its main sections once, in source order. No stale or missing chapter-opening item remains.

| Chapter | Opening page | Main sections checked | Result |
|---|---:|---:|---|
| 1 - Strategic Vision and Project Scope | 1 | 6 | PASS |
| 2 - Literature Review and Theoretical Framework | 7 | 6 | PASS |
| 3 - Methodology | 15 | 4 | PASS |
| 4 - System Analysis and Requirements | 20 | 8 | PASS |
| 5 - System Design | 60 | 4 | PASS |
| 6 - Software and Engineering Implementation | 108 | 14 | PASS; all entries fit on the opening page |
| 7 - System Testing and Evaluation | 118 | 5 | PASS |
| 8 - Future Work and Recommendations | 121 | 4 | PASS |

Chapter 3 has exactly the requested hierarchy:

| Number | Heading | Printed page |
|---|---|---:|
| 3.1 | Introduction | 16 |
| 3.2 | Methodological Approach | 16 |
| 3.2.1 | Iterative Feature-Centered Development | 16 |
| 3.2.2 | Vertical-Slice Realization | 17 |
| 3.2.3 | Why This Methodology Fits EduVerse | 17 |
| 3.3 | Repeated Development Cycle | 18 |
| 3.4 | Chapter Summary | 19 |

Its four opening targets resolve as follows:

| Label | Resolved heading | Printed page |
|---|---|---:|
| `sec:methodology_introduction` | 3.1 Introduction | 16 |
| `sec:system_development_methodology` | 3.2 Methodological Approach | 16 |
| `sec:development_workflow_structure` | 3.3 Repeated Development Cycle | 18 |
| `sec:chapter3_summary` | 3.4 Chapter Summary | 19 |

## D. List of Figures

**Correct: all 52 figures verified.** Figures 4.1-4.26 and 5.1-5.26 have matching source captions, visible captions, figure numbers, List of Figures rows, destinations, and actual printed pages. There are no missing, duplicate, stale, misnumbered, or incorrectly paginated entries. Every indexed caption was also located independently in the body.

No figure changed page relative to the closest old PDF or the saved pre-audit PDF. Figures remain within their chapters, with their captions attached to the corresponding objects. The appendix records every figure's final printed page.

## E. List of Tables

**Correct: all 38 tables verified.** This includes Table 2.1, Table 3.1, Table 4.1, Tables 5.1-5.34, and Table 6.1. Numbering, captions, order, visible list entries, destinations, and actual printed pages agree. No missing, duplicate, stale, or mismatched entries remain.

**Table 3.1, "Repeated Iterative Development Structure in EduVerse", appears on printed page 18, and the List of Tables correctly shows 18.** Its introduction, caption, and complete six-stage table appear together on that page.

For multipage longtables, the list correctly points to the first page bearing the caption. A continuation page does not require a new List of Tables entry. Table 6.1 is correctly listed on 110; its placement is discussed separately in section H.

## F. Cross-References and Labels

Final checks found:

- 138 active labels, each matching its source attachment and generated auxiliary record.
- 78 explicit reference/chapter-opening target uses, with no undefined target.
- 23 citation-key uses covering all 14 bibliography keys, with no undefined citation.
- 321 internal PDF link annotations, with no missing destination.
- No duplicate or multiply defined labels, unsafe label names, obsolete auxiliary labels, wrong numbered attachments, or visible `??` anywhere in the PDF.
- No reference-related, citation-related, duplicate-destination, or rerun warning in the final compilation log. BibTeX completed successfully without a warning or error.

Some valid labels are unused; unused alone is not evidence that a label is stale. The two actual label defects were repaired as detailed in section I. Three literal chapter references in Chapter 6 also refer to the correct chapters.

## G. Pagination Changes

The closest relevant old PDF is the `main.pdf` committed at Git HEAD `8e91984` (PDF creation metadata: 10 September 2026). Its contents isolate the recent Chapter 3 change: one additional sentence in section 3.2. Older July and early-September PDFs contain other revisions and are not used to decide what the current pages should be.

| Item | Closest old PDF | Final PDF | Classification |
|---|---:|---:|---|
| Chapter 3 opening | 15 | 15 | Unchanged |
| 3.1 and 3.2 | 16 | 16 | Unchanged |
| 3.2.1 | 16 | 16 | Start unchanged; paragraph continuation reflows onto 17 |
| 3.2.2 and 3.2.3 | 17 | 17 | Unchanged starts |
| 3.3 Repeated Development Cycle | 17 | 18 | **EXPECTED SHIFT**; both TOC and opening contents show 18 |
| Table 3.1 | 18 | 18 | Unchanged |
| Version-control paragraph following Table 3.1 | 18 | 19 | **EXPECTED SHIFT**; remains before section 3.4 |
| 3.4 Chapter Summary | 19 | 19 | Unchanged |
| Chapter 4 | 20 | 20 | Unchanged |
| Chapter 5 | 60 | 60 | Unchanged |
| Chapter 6 | 108 | 108 | Unchanged |
| Chapter 7 | 118 | 118 | Unchanged |
| Chapter 8 | 121 | 121 | Unchanged |
| Conclusion | 123 | 123 | Unchanged |
| References | 124 | 124 | Unchanged |
| Final printed page | 125 | 125 | Unchanged |

Across the 177 numbered chapter/section/subsection/figure/table destinations, **only section 3.3 changes page**. No later chapter, section, figure, or table shifts. There is no actual pagination inconsistency. The cover is unnumbered; Roman numbering i-xi changes cleanly to Arabic 1, without a repeated or skipped printed body page.

Compared with the already-updated PDF present at the start of this audit, the final rebuilt PDF has **no changed page destinations, no changed extracted page text, and no changed rendered pixels on any of its 137 pages** at the same 72-dpi rendering settings. Thus the technical label repairs did not change pagination or visible content.

## H. Structural / Paragraph / Float Issues

### Chapter 3 and overall reading flow

Chapter 3's source and rendered pages preserve the intended paragraph sequence. The added sentence remains in section 3.2. The paragraph spanning pages 16-17 continues naturally in section 3.2.1; section 3.3 and its two introductory paragraphs precede Table 3.1 on 18; the version-control paragraph follows the table on 19 before section 3.4. No paragraph, heading, table row, or caption was duplicated, omitted, or reordered by the recent edit or the audit fixes.

The source comparison with the closest baseline and the rendered-text comparison support this finding. No exact duplicate was found among 197 substantial prose paragraphs screened. There are no blank inserted pages, figures or tables crossing unintentionally into a later chapter, separated object/caption pairs, or numbered headings stranded without their following text in the reviewed rendering. Large clear areas on chapter-opening pages and some float pages are existing layout behavior, not evidence of a stale index.

### Pre-existing minor findings retained

1. **Table 6.1 appears after section 6.3 begins.** It is introduced in section 6.2 on page 109 but occupies page 110, after the section 6.3 text on 109. The source is `chapters/chapter6_implementation.tex:38` (`\begin{table}[htbp]`); the `\FloatBarrier` at line 68 has no effect because `main.tex:25` defines it as an empty command. This is ordinary deferred-float behavior and a minor reading-order caveat. The table follows its introduction, remains in Chapter 6, and its reference and List of Tables entry correctly identify it. No placement override was applied.

2. **Isolated horizontal table rules appear near the top of pages 69 and 82.** These are visible at the longtable boundaries following Table 5.8 on page 68 and Table 5.33 on page 81. Relevant source: `chapters/chapter5_system_design.tex:45-57`, the shared `\EduSchemaRow` / `\EduSchemaTableEnd` macros, and the table endings at lines 371 and 769. Their appearance is consistent with a final rule carried across a longtable page boundary. The rows, captions, table numbers, and list pages remain complete and correct. These cosmetic border artifacts predate the audit and were not changed.

3. **Existing typesetting diagnostics remain.** The final log has 2 overfull boxes, 124 underfull boxes, and 12 nonfatal `ignored error: Infinite glue shrinkage found in box being split` diagnostics at longtable page breaks. These counts exactly match the saved pre-audit log. The two overfull boxes are 2.86642 pt in Chapter 2's Table 2.1 (`chapters/chapter2_literature_review.tex:172`, the word "Communication") and 4.78584 pt in Chapter 4's FR-17 paragraph (`chapters/chapter4_system_analysis.tex:159-162`). They are minor existing typesetting defects, not reference failures. The repeated clean-build commands all exit successfully, and the final rendering retains all content. No typography, spacing, column-width, or margin change was made to suppress them.

These findings justify PASS WITH MINOR ISSUES instead of an unqualified presentation pass. No additional source change is required for index/reference consistency. The audit does not claim that the entire typesetting log is free of diagnostics.

## I. Required Fixes

Both required technical repairs have been applied; no further indexing/reference repair is outstanding.

### 1. Malformed Chapter 5 label - fixed

- **Source:** `chapters/chapter5_system_design.tex:296`.
- **Original command:** `\label{*subsec\:database\_tables*}`.
- **Original behavior/cause:** escaped LaTeX commands inside the label key expand while the generated auxiliary record is reread, producing `Missing \endcsname inserted`. A clean build with `-halt-on-error` stopped at this record.
- **Expected behavior:** a plain, stable label key identifying subsection 5.3.4, Physical Schema Tables, on page 66.
- **Exact minimal fix applied:** `\label{subsec:database_tables}`.
- **Verification:** the key is unique, its title/number/page/anchor agree with subsection 5.3.4, and the build now rereads the auxiliary files successfully. No existing reference used the malformed key, so no reference call needed changing.

### 2. Inherited numeric value on the unnumbered Conclusion label - fixed

- **Source:** `backmatter/conclusion.tex:1`.
- **Original command:** `\chapter*{Conclusion}\label{chap:conclusion}`.
- **Original behavior/cause:** `\chapter*` does not step the numbered chapter counter; the label inherited the preceding section's numeric reference value, 8.4. Its page/name destination was correct, and it was unused, so this had not produced a visible wrong reference.
- **Expected behavior:** no misleading numbered reference attached to an intentionally unnumbered heading.
- **Exact minimal fix applied:** remove the unused `\label{chap:conclusion}`, leaving `\chapter*{Conclusion}` and the existing `\addcontentsline` unchanged.
- **Verification:** no source reference targets this removed key. Conclusion still begins on 123, with its correct TOC entry and clickable destination.

Only these two thesis source files changed during the audit. Source hashes confirm that Chapter 3 and every other source/bibliography file remained unchanged by the audit. The retained presentation notes in section H are not required indexing fixes and were not used as a reason to redesign the thesis.

## J. Final Verification

The project uses the README's **pdflatex + BibTeX** build method. The initial clean build diagnosed the malformed label. A Windows PDF write lock and MiKTeX's search for root auxiliary files during an output-directory-only attempt were resolved by building a staged copy of the unchanged project sources and assets in a clean working directory.

The final successful sequence was:

```text
pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -recorder main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -recorder main.tex
pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -recorder main.tex
pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -recorder main.tex
```

All five commands exited 0. The final two LaTeX passes produced identical hashes for `.aux`, `.toc`, `.lof`, `.lot`, `.out`, `.bbl`, and all included auxiliary records. The stable PDF and generated build files were copied back to the project root. The historical PDFs and original pre-audit PDF were preserved.

Final verification covered all 137 physical pages; all 136 printed Roman/Arabic page numbers matched the PDF page labels; all 184 TOC/LOF/LOT entries matched their actual printed pages; all 51 opening-list entries resolved correctly; all 90 body captions were located; all 138 labels passed attachment/page/number checks; all 321 internal links had valid destinations. The automated final consistency audit returned **zero issues**. Visual inspection included the index pages, chapter openings, complete Chapter 3, later figure/table flow, longtable continuations, Conclusion, and References. A full-page raster comparison additionally confirmed zero visual changes from the saved pre-audit PDF after the label repairs.

**Final verdict: the current source, final compiled PDF, TOC, chapter-opening contents, LOF, LOT, references, and printed page numbers are mutually consistent.**

### Evidence

- Final output: project-root `main.pdf`.
- Per-entry ledger: `docs/structural-pagination-index-verification-2026-09-23.csv`.
- Detailed PDF checks: `tmp/audit-20260923/pdf-audit.json`.
- Source inventory: `tmp/audit-20260923/source-audit/source-audit.json`.
- Build commands, logs, and stability hashes: `tmp/audit-20260923/build-evidence-staged/`.
- Render/text regression checks: `tmp/audit-20260923/final-visual/render-verification.json`.
- Preserved old/current-baseline comparison: `tmp/audit-20260923/baseline-audit/`.
'''
report+='\nFinal PDF SHA-256: `'+hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()+'`.\n'
for ext,title in [('toc','Appendix 1: every main TOC entry'),('lof','Appendix 2: every figure'),('lot','Appendix 3: every table')]:
    report+=f'\n## {title}\n\nAll rows below passed source/title/number/order and final-PDF printed-page checks.\n\n| Number | Title | Printed page | Result |\n|---|---|---:|---|\n'
    for entry in pdf['entries']:
        if entry['list']==ext:
            title=entry['title'].replace('|','\\|')
            report+=f"| {entry['number'] or 'Unnumbered'} | {title} | {entry['actual_printed_page']} | PASS |\n"
report+='\n## Appendix 4: every chapter-opening item\n\n| Chapter | Label | Resolved number and title | Printed page | Result |\n|---:|---|---|---:|---|\n'
for entry in pdf['opening_checks']:
    report+=f"| {entry['chapter']} | `{entry['key']}` | {entry['number']} {entry['title']} | {entry['page']} | PASS |\n"
OUT.write_text(report,encoding='utf-8')
shutil.copy2(AUDIT/'index-verification.csv',ROOT/'docs/structural-pagination-index-verification-2026-09-23.csv')
print(OUT)
print('Report includes A-J plus all 184 index entries and all 51 chapter-opening entries.')
