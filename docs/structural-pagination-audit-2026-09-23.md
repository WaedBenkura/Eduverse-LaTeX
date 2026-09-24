# EduVerse thesis: final structural and pagination audit

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

Final PDF SHA-256: `47bf9853c21b1032cf2fb744f4efd73e20fe5e0dbc3251c131b71cb2db8ab051`.

## Appendix 1: every main TOC entry

All rows below passed source/title/number/order and final-PDF printed-page checks.

| Number | Title | Printed page | Result |
|---|---|---:|---|
| Unnumbered | Abstract | i | PASS |
| Unnumbered | Acknowledgements | ii | PASS |
| Unnumbered | Contents | iii | PASS |
| Unnumbered | List of Figures | vii | PASS |
| Unnumbered | List of Tables | x | PASS |
| 1 | Strategic Vision and Project Scope | 1 | PASS |
| 1.1 | Project Vision | 2 | PASS |
| 1.2 | Problem Statement | 2 | PASS |
| 1.3 | Project Motivations | 3 | PASS |
| 1.4 | Strategic Objectives | 3 | PASS |
| 1.5 | Project Benefits and Broader Impact | 4 | PASS |
| 1.6 | Project Scope and Boundaries | 5 | PASS |
| 1.6.1 | System Boundaries and User Roles | 5 | PASS |
| 1.6.2 | Functional Scope | 5 | PASS |
| 1.6.3 | Web and Mobile Client Scope | 6 | PASS |
| 1.6.4 | Distinctive Features and Extensible Design | 6 | PASS |
| 2 | Literature Review and Theoretical Framework | 7 | PASS |
| 2.1 | Introduction | 8 | PASS |
| 2.2 | Evolution of Digital Education Platforms | 8 | PASS |
| 2.2.1 | From Traditional Classroom Management to Digital Learning Systems | 8 | PASS |
| 2.2.2 | Limitations of Fragmented Learning Management Tools | 9 | PASS |
| 2.3 | Research Gap and Integrated Learning Ecosystems | 9 | PASS |
| 2.4 | Artificial Intelligence in Education | 10 | PASS |
| 2.4.1 | Context-Aware Learning Assistance | 10 | PASS |
| 2.4.2 | Material Summarization and Learning Support | 10 | PASS |
| 2.4.3 | Assessment and Feedback Support | 10 | PASS |
| 2.5 | Benchmarking: Fragmented Tools vs. Integrated EduVerse Approach | 11 | PASS |
| 2.6 | Theoretical and Technical Foundations of EduVerse | 12 | PASS |
| 2.6.1 | Web-Based Educational Platforms | 12 | PASS |
| 2.6.2 | Mobile Companion Learning Applications | 13 | PASS |
| 2.6.3 | Real-Time Virtual Classrooms | 13 | PASS |
| 2.6.4 | Integrated Coding Environments for Programming Education | 13 | PASS |
| 2.6.5 | Extensible Educational Ecosystems and Governed Openness | 14 | PASS |
| 2.6.6 | Security, Roles, and Data Management | 14 | PASS |
| 3 | Methodology | 15 | PASS |
| 3.1 | Introduction | 16 | PASS |
| 3.2 | Methodological Approach | 16 | PASS |
| 3.2.1 | Iterative Feature-Centered Development | 16 | PASS |
| 3.2.2 | Vertical-Slice Realization | 17 | PASS |
| 3.2.3 | Why This Methodology Fits EduVerse | 17 | PASS |
| 3.3 | Repeated Development Cycle | 18 | PASS |
| 3.4 | Chapter Summary | 19 | PASS |
| 4 | System Analysis and Requirements | 20 | PASS |
| 4.1 | Introduction | 21 | PASS |
| 4.2 | System Overview | 21 | PASS |
| 4.3 | System Actors | 21 | PASS |
| 4.4 | Functional Requirements | 22 | PASS |
| 4.5 | Non-Functional Requirements | 27 | PASS |
| 4.6 | Use-Case Model | 28 | PASS |
| 4.7 | Activity Diagrams | 44 | PASS |
| 4.8 | Chapter Summary | 59 | PASS |
| 5 | System Design | 60 | PASS |
| 5.1 | Introduction | 61 | PASS |
| 5.2 | Design Context and Architectural Structure | 61 | PASS |
| 5.3 | Information Model and Persistence Design | 61 | PASS |
| 5.3.1 | Logical Database Design | 62 | PASS |
| 5.3.2 | Relational Structure Through the ERD | 62 | PASS |
| 5.3.3 | Principal Schema Groups | 65 | PASS |
| 5.3.4 | Physical Schema Tables | 66 | PASS |
| 5.4 | Interface and Interaction Design | 82 | PASS |
| 5.4.1 | Access and Identity Interfaces | 82 | PASS |
| 5.4.2 | Administrative Governance Interfaces | 86 | PASS |
| 5.4.3 | Classroom and Learning Interfaces | 94 | PASS |
| 5.4.4 | Assessment and Submission Interfaces | 98 | PASS |
| 5.4.5 | Synchronous Collaboration Interfaces | 105 | PASS |
| 5.4.6 | AI Support and Coding-Lab Interfaces | 106 | PASS |
| 6 | Software and Engineering Implementation | 108 | PASS |
| 6.1 | Introduction | 109 | PASS |
| 6.2 | Implementation Environment | 109 | PASS |
| 6.3 | System Architecture | 109 | PASS |
| 6.4 | Web Application Implementation | 111 | PASS |
| 6.5 | Mobile Companion Application Implementation | 111 | PASS |
| 6.6 | Backend, Database, and Storage Implementation | 112 | PASS |
| 6.7 | Authentication, Authorization, and Security | 113 | PASS |
| 6.8 | Role-Based and Multi-Organization Access | 113 | PASS |
| 6.9 | Feature Availability and Extension Implementation | 114 | PASS |
| 6.10 | Real-Time Communication and Live Sessions | 114 | PASS |
| 6.11 | AI Learning Support and IDE Implementation | 115 | PASS |
| 6.12 | Development Workflow and Deployment | 116 | PASS |
| 6.13 | Implementation Challenges and Adopted Solutions | 116 | PASS |
| 6.14 | Chapter Summary | 117 | PASS |
| 7 | System Testing and Evaluation | 118 | PASS |
| 7.1 | Introduction | 119 | PASS |
| 7.2 | Testing Strategy | 119 | PASS |
| 7.3 | Functional Testing | 119 | PASS |
| 7.4 | Non-Functional Evaluation | 119 | PASS |
| 7.5 | Review and Evaluation Summary | 120 | PASS |
| 8 | Future Work and Recommendations | 121 | PASS |
| 8.1 | Introduction | 122 | PASS |
| 8.2 | Scalability Improvements | 122 | PASS |
| 8.3 | User Feedback and Usability Refinement | 122 | PASS |
| 8.4 | Chapter Summary | 122 | PASS |
| Unnumbered | Conclusion | 123 | PASS |
| Unnumbered | References | 124 | PASS |

## Appendix 2: every figure

All rows below passed source/title/number/order and final-PDF printed-page checks.

| Number | Title | Printed page | Result |
|---|---|---:|---|
| 4.1 | Project Overview Use-Case Diagram | 31 | PASS |
| 4.2 | Authentication and Access Use-Case Diagram | 32 | PASS |
| 4.3 | Organization and Role Management Use-Case Diagram | 33 | PASS |
| 4.4 | Class Management Use-Case Diagram | 34 | PASS |
| 4.5 | Assignment Management Use-Case Diagram | 35 | PASS |
| 4.6 | AI Learning Support Use-Case Diagram | 36 | PASS |
| 4.7 | Class Communication and Notifications Use-Case Diagram | 37 | PASS |
| 4.8 | Course Content and Materials Use-Case Diagram | 38 | PASS |
| 4.9 | Exam Management and Integrity Use-Case Diagram | 39 | PASS |
| 4.10 | Live Sessions and Whiteboard Use-Case Diagram | 40 | PASS |
| 4.11 | Integrated Coding Lab / IDE Extension Use-Case Diagram | 41 | PASS |
| 4.12 | Profile and Help Use-Case Diagram | 42 | PASS |
| 4.13 | Results and Dashboards Use-Case Diagram | 43 | PASS |
| 4.14 | Authentication and Workspace Access Activity Diagram | 46 | PASS |
| 4.15 | Organization Member Access and Public Join Link Activity Diagram | 47 | PASS |
| 4.16 | Class Creation, Configuration, and Past Terms Activity Diagram | 48 | PASS |
| 4.17 | Course Content and Materials Activity Diagram | 49 | PASS |
| 4.18 | Class Communication and Notifications Activity Diagram | 50 | PASS |
| 4.19 | Assignment Workflow Activity Diagram | 51 | PASS |
| 4.20 | Exam Management and Integrity Workflow Activity Diagram | 52 | PASS |
| 4.21 | Live Session and Whiteboard Workflow Activity Diagram | 53 | PASS |
| 4.22 | Results Workflow Activity Diagram | 54 | PASS |
| 4.23 | Dashboard Workflow Activity Diagram | 55 | PASS |
| 4.24 | AI Learning Support Workflow Activity Diagram | 56 | PASS |
| 4.25 | Integrated Coding Lab / IDE Workflow Activity Diagram | 57 | PASS |
| 4.26 | Profile and Help Workflow Activity Diagram | 58 | PASS |
| 5.1 | Entity Relationship Diagram of the EduVerse Database | 64 | PASS |
| 5.2 | Authentication interface showing sign-in and sign-up forms for EduVerse users. | 83 | PASS |
| 5.3 | Organization and active-role selector used to switch between available EduVerse workspaces. | 84 | PASS |
| 5.4 | User profile and settings interface showing role context, theme preferences, and password management controls. | 85 | PASS |
| 5.5 | Organization creation interface showing template-based setup and initial feature-availability controls for different educational contexts. | 87 | PASS |
| 5.6 | Organization administrator dashboard showing class oversight and organization-wide statistics. | 88 | PASS |
| 5.7 | Class creation and feature-configuration dialog used to define class properties and enabled tools. | 89 | PASS |
| 5.8 | Past-terms administration interface used to review archived classes and historical academic records. | 90 | PASS |
| 5.9 | Organization members and invitations interface showing role assignment and invitation-management controls. | 91 | PASS |
| 5.10 | Public join-link management interface showing join-link creation and request-handling controls. | 91 | PASS |
| 5.11 | Public join page used by a student to request access to an organization workspace. | 92 | PASS |
| 5.12 | Organization settings interface showing public-feature controls and teacher class-permission settings. | 93 | PASS |
| 5.13 | Class home interface showing the main classroom workspace and available learning tools. | 94 | PASS |
| 5.14 | Classroom materials interface used to access uploaded learning resources and study actions. | 95 | PASS |
| 5.15 | Class chat and announcements interface supporting class-wide discussion and instructor notices. | 96 | PASS |
| 5.16 | Notifications panel showing alerts for live sessions, materials, examinations, and announcements. | 97 | PASS |
| 5.17 | Assignment management interface showing teacher-side assignment creation, submission review, and grading controls. | 98 | PASS |
| 5.18 | Student assignment submission interface showing response entry and file-upload controls. | 99 | PASS |
| 5.19 | Exam management interface showing teacher-side exam creation and question configuration. | 100 | PASS |
| 5.20 | Student exam start interface showing exam rules, timing, and attempt conditions before entry. | 101 | PASS |
| 5.21 | Student exam-taking interface showing timed question navigation during an active exam attempt. | 102 | PASS |
| 5.22 | Exam attempt review interface showing submitted answers, grading controls, and integrity-related events. | 103 | PASS |
| 5.23 | Results dashboard showing released grades, score breakdowns, and detailed assessment feedback. | 104 | PASS |
| 5.24 | Live session room showing the shared whiteboard, participant list, and session controls. | 105 | PASS |
| 5.25 | AI learning support interface showing conversational assistance within the class workspace. | 106 | PASS |
| 5.26 | Integrated coding workspace showing the file explorer, code editor, terminal, and live preview pane. | 107 | PASS |

## Appendix 3: every table

All rows below passed source/title/number/order and final-PDF printed-page checks.

| Number | Title | Printed page | Result |
|---|---|---:|---|
| 2.1 | Fragmented Educational Tools vs. Integrated EduVerse Approach | 11 | PASS |
| 3.1 | Repeated Iterative Development Structure in EduVerse | 18 | PASS |
| 4.1 | Primary EduVerse System Actors | 22 | PASS |
| 5.1 | Principal Schema Groups in EduVerse | 65 | PASS |
| 5.2 | Schema for Table: organizations | 66 | PASS |
| 5.3 | Schema for Table: profiles | 66 | PASS |
| 5.4 | Schema for Table: organization_memberships | 67 | PASS |
| 5.5 | Schema for Table: organization_membership_roles | 67 | PASS |
| 5.6 | Schema for Table: organization_invites | 67 | PASS |
| 5.7 | Schema for Table: organization_settings | 68 | PASS |
| 5.8 | Schema for Table: organization_teacher_class_permissions | 68 | PASS |
| 5.9 | Schema for Table: organization_join_links | 69 | PASS |
| 5.10 | Schema for Table: organization_join_requests | 69 | PASS |
| 5.11 | Schema for Table: class_invites | 70 | PASS |
| 5.12 | Schema for Table: classes | 70 | PASS |
| 5.13 | Schema for Table: class_memberships | 71 | PASS |
| 5.14 | Schema for Table: class_visibility_preferences | 71 | PASS |
| 5.15 | Schema for Table: feature_definitions | 72 | PASS |
| 5.16 | Schema for Table: feature_presets | 72 | PASS |
| 5.17 | Schema for Table: feature_preset_items | 72 | PASS |
| 5.18 | Schema for Table: organization_feature_settings | 73 | PASS |
| 5.19 | Schema for Table: class_feature_settings | 73 | PASS |
| 5.20 | Schema for Table: organization_extensions | 73 | PASS |
| 5.21 | Schema for Table: class_extension_settings | 74 | PASS |
| 5.22 | Schema for Table: class_materials | 74 | PASS |
| 5.23 | Schema for Table: class_messages | 75 | PASS |
| 5.24 | Schema for Table: class_assignments | 76 | PASS |
| 5.25 | Schema for Table: class_assignment_files | 76 | PASS |
| 5.26 | Schema for Table: class_assignment_submissions | 77 | PASS |
| 5.27 | Schema for Table: exams | 78 | PASS |
| 5.28 | Schema for Table: exam_questions | 78 | PASS |
| 5.29 | Schema for Table: exam_attempts | 79 | PASS |
| 5.30 | Schema for Table: exam_answers | 80 | PASS |
| 5.31 | Schema for Table: notifications | 80 | PASS |
| 5.32 | Schema for Table: class_live_sessions | 81 | PASS |
| 5.33 | Schema for Table: audit_logs | 81 | PASS |
| 5.34 | Schema for Table: auth.users | 82 | PASS |
| 6.1 | Main EduVerse Implementation Environment | 110 | PASS |

## Appendix 4: every chapter-opening item

| Chapter | Label | Resolved number and title | Printed page | Result |
|---:|---|---|---:|---|
| 1 | `sec:project_vision` | 1.1 Project Vision | 2 | PASS |
| 1 | `sec:problem_statement` | 1.2 Problem Statement | 2 | PASS |
| 1 | `sec:project_motivations` | 1.3 Project Motivations | 3 | PASS |
| 1 | `sec:strategic_objectives` | 1.4 Strategic Objectives | 3 | PASS |
| 1 | `sec:team_goals` | 1.5 Project Benefits and Broader Impact | 4 | PASS |
| 1 | `sec:project_scope` | 1.6 Project Scope and Boundaries | 5 | PASS |
| 2 | `sec:literature_review_introduction` | 2.1 Introduction | 8 | PASS |
| 2 | `sec:evolution_of_digital_education_platforms` | 2.2 Evolution of Digital Education Platforms | 8 | PASS |
| 2 | `sec:research_gap_integrated_ecosystem` | 2.3 Research Gap and Integrated Learning Ecosystems | 9 | PASS |
| 2 | `sec:artificial_intelligence_in_education` | 2.4 Artificial Intelligence in Education | 10 | PASS |
| 2 | `sec:benchmarking_fragmented_vs_integrated` | 2.5 Benchmarking: Fragmented Tools vs. Integrated EduVerse Approach | 11 | PASS |
| 2 | `sec:theoretical_technical_foundations_eduverse` | 2.6 Theoretical and Technical Foundations of EduVerse | 12 | PASS |
| 3 | `sec:methodology_introduction` | 3.1 Introduction | 16 | PASS |
| 3 | `sec:system_development_methodology` | 3.2 Methodological Approach | 16 | PASS |
| 3 | `sec:development_workflow_structure` | 3.3 Repeated Development Cycle | 18 | PASS |
| 3 | `sec:chapter3_summary` | 3.4 Chapter Summary | 19 | PASS |
| 4 | `sec:system_analysis_introduction` | 4.1 Introduction | 21 | PASS |
| 4 | `sec:system_overview` | 4.2 System Overview | 21 | PASS |
| 4 | `sec:system_actors` | 4.3 System Actors | 21 | PASS |
| 4 | `sec:functional_requirements` | 4.4 Functional Requirements | 22 | PASS |
| 4 | `sec:non_functional_requirements` | 4.5 Non-Functional Requirements | 27 | PASS |
| 4 | `sec:use_case_model` | 4.6 Use-Case Model | 28 | PASS |
| 4 | `sec:activity_diagrams` | 4.7 Activity Diagrams | 44 | PASS |
| 4 | `sec:chapter4_summary` | 4.8 Chapter Summary | 59 | PASS |
| 5 | `sec:system_design_introduction` | 5.1 Introduction | 61 | PASS |
| 5 | `sec:architectural_design_overview` | 5.2 Design Context and Architectural Structure | 61 | PASS |
| 5 | `sec:data_and_storage_design` | 5.3 Information Model and Persistence Design | 61 | PASS |
| 5 | `sec:interface_and_interaction_design` | 5.4 Interface and Interaction Design | 82 | PASS |
| 6 | `sec:implementation_introduction` | 6.1 Introduction | 109 | PASS |
| 6 | `sec:implementation_environment` | 6.2 Implementation Environment | 109 | PASS |
| 6 | `sec:implementation_system_architecture` | 6.3 System Architecture | 109 | PASS |
| 6 | `sec:web_application_implementation` | 6.4 Web Application Implementation | 111 | PASS |
| 6 | `sec:mobile_companion_application_implementation` | 6.5 Mobile Companion Application Implementation | 111 | PASS |
| 6 | `sec:backend_database_storage_implementation` | 6.6 Backend, Database, and Storage Implementation | 112 | PASS |
| 6 | `sec:authentication_authorization_security` | 6.7 Authentication, Authorization, and Security | 113 | PASS |
| 6 | `sec:role_based_multi_organization_access` | 6.8 Role-Based and Multi-Organization Access | 113 | PASS |
| 6 | `sec:feature_availability_extension_implementation` | 6.9 Feature Availability and Extension Implementation | 114 | PASS |
| 6 | `sec:real_time_communication_live_sessions` | 6.10 Real-Time Communication and Live Sessions | 114 | PASS |
| 6 | `sec:ai_learning_support_ide_implementation` | 6.11 AI Learning Support and IDE Implementation | 115 | PASS |
| 6 | `sec:development_workflow_deployment` | 6.12 Development Workflow and Deployment | 116 | PASS |
| 6 | `sec:implementation_challenges_adopted_solutions` | 6.13 Implementation Challenges and Adopted Solutions | 116 | PASS |
| 6 | `sec:implementation_chapter_summary` | 6.14 Chapter Summary | 117 | PASS |
| 7 | `sec:testing_evaluation_introduction` | 7.1 Introduction | 119 | PASS |
| 7 | `sec:testing_strategy` | 7.2 Testing Strategy | 119 | PASS |
| 7 | `sec:functional_testing` | 7.3 Functional Testing | 119 | PASS |
| 7 | `sec:non_functional_evaluation` | 7.4 Non-Functional Evaluation | 119 | PASS |
| 7 | `sec:review_evaluation_summary` | 7.5 Review and Evaluation Summary | 120 | PASS |
| 8 | `sec:future_work_introduction` | 8.1 Introduction | 122 | PASS |
| 8 | `sec:scalability_improvements` | 8.2 Scalability Improvements | 122 | PASS |
| 8 | `sec:user_feedback_usability_refinement` | 8.3 User Feedback and Usability Refinement | 122 | PASS |
| 8 | `sec:future_work_summary` | 8.4 Chapter Summary | 122 | PASS |
