# Baseline comparison audit

The original root `main.pdf` was preserved before the audit rebuild as `../baseline-main.pdf`; its corresponding root `.aux`, `.toc`, `.lof`, `.lot`, `.out`, and `.log` files were preserved in this directory. No thesis source was changed by this subtask.

## Baselines available

| Baseline | PDF creation date | Physical pages | Relevance |
|---|---|---:|---|
| Pre-audit root `main.pdf` | 2026-09-23 20:58:39 +02:00 | 137 | Already contains the current Chapter 3 sentence and refreshed indexes. |
| Git HEAD (`8e91984`) root `main.pdf` | 2026-09-10 11:30:09 +02:00 | 137 | Best available old PDF for isolating the recent Chapter 3 modification. |
| `output/pdf/main.pdf` | 2026-09-02 07:53:31 +02:00 | 142 | Older full thesis; differences include unrelated revisions. |
| `build/main.pdf` | 2026-07-06 00:55:24 +02:00 | 149 | Older full thesis; differences include unrelated revisions. |
| `thesischeck.pdf` | 2026-07-06 00:56:28 +02:00 | 141 | Older intermediate build, with incomplete front matter compared with later builds. |
| `thesisfinalcheck.pdf` | 2026-07-06 00:57:59 +02:00 | 150 | Older full thesis; differences include unrelated revisions. |
| `thesisfinalcheck2.pdf` | 2026-07-06 01:01:58 +02:00 | 150 | Older full thesis; differences include unrelated revisions. |

Creation dates are PDF metadata, not filesystem modification timestamps. Git HEAD is a September 12 commit, but the committed PDF records September 10 creation. Text comparison validates its relevance despite that timestamp difference: the only changed thesis body text is the added sentence in section 3.2 and resulting Chapter 3 reflow.

## Source change versus HEAD

`git diff -- chapters/chapter3_methodology.tex` identifies only an added sentence in section 3.2, Methodological Approach: “Initial requirements were identified primarily through the project team’s prior life experience with educational and digital learning environments.” The blank source line before the next subsection also changed. No other thesis source differs from HEAD.

## Pagination comparison: HEAD versus pre-audit PDF

All pages below are thesis page labels, not raw PDF indices. There is one unnumbered cover, front matter i–xi, and body pages 1–125 (137 physical pages total).

| Item | HEAD | Pre-audit current | Classification |
|---|---:|---:|---|
| Chapter 3 Methodology | 15 | 15 | Unchanged |
| 3.1 Introduction | 16 | 16 | Unchanged |
| 3.2 Methodological Approach | 16 | 16 | Unchanged |
| 3.2.1 Iterative Feature-Centered Development | 16 | 16 | Unchanged start; final two lines continue on p.17 |
| 3.2.2 Vertical-Slice Realization | 17 | 17 | Unchanged |
| 3.2.3 Why This Methodology Fits EduVerse | 17 | 17 | Unchanged |
| 3.3 Repeated Development Cycle | 17 | 18 | **EXPECTED SHIFT**; TOC and chapter-opening contents both show current p.18 |
| Table 3.1 Repeated Iterative Development Structure in EduVerse | 18 | 18 | Unchanged |
| Version-control paragraph following Table 3.1 | 18 | 19 | **EXPECTED SHIFT**; remains before section 3.4 |
| 3.4 Chapter Summary | 19 | 19 | Unchanged |
| Chapter 4 | 20 | 20 | Unchanged |
| Chapter 5 | 60 | 60 | Unchanged |
| Chapter 6 | 108 | 108 | Unchanged |
| Chapter 7 | 118 | 118 | Unchanged |
| Chapter 8 | 121 | 121 | Unchanged |
| Conclusion | 123 | 123 | Unchanged |
| References | 124 | 124 | Unchanged |
| Final body page | 125 | 125 | Unchanged |

The numbered destination inventories in both PDFs are identical: 8 chapters, 51 sections, 28 subsections, 52 figures, and 38 tables. Of these 177 destinations, only section 3.3 changes page. No figure or table changes page. No destination was removed or added. Unnumbered Conclusion and References destinations are also unchanged.

Full-page extracted text comparison confirms that every page after Chapter 3, from thesis p.20 through p.125, is unchanged. Across the whole PDF, the only changed pages are TOC p.iv and Chapter 3 pp.15–19. The TOC and Chapter 3 opening list both correctly change the reference to section 3.3 from p.17 to p.18. See `head-to-preaudit-text.diff` for the exact page-by-page changes.

Chapter 3 body reflow preserves the paragraph sequence: the mobile-companion paragraph continues across pp.16–17; section 3.3 and its two introductory paragraphs begin on p.18 ahead of Table 3.1; the version-control paragraph continues on p.19 before section 3.4. Text extraction shows no omission, duplication, or reordering. Visual review is handled in the main audit.

## Why other PDFs must not define the current expected pagination

The July PDFs have 57 section destinations and 37 table destinations; the current PDF has 51 and 38. The September 2 PDF has 27 subsections and 37 tables; the current PDF has 28 and 38. Their broader page differences therefore reflect other historical content/structure changes. They are useful archival baselines but cannot isolate the recent Chapter 3 edit. No current inconsistency should be inferred merely because their page numbers differ.

## Machine-readable evidence

- `baselines.json`: full PDF metadata, checksums, page labels, destination/page mapping, and Chapter 3 text for all available baseline PDFs.
- `baseline-comparisons.json`: destination-by-destination differences between each historical PDF and the comparison target.
- `head-to-preaudit-text.diff`: complete extracted-text differences between the closest old PDF and the preserved pre-audit PDF.
- `head-to-preaudit-text-pages.json`: pages with differences.
- `git-head-main.pdf` and `git-head-chapter3.tex`: read-only baseline snapshots extracted from Git.

The final rebuilt PDF must additionally be compared with the preserved pre-audit PDF once the main audit build is complete.
