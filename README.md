# EduVerse Thesis Documentation

This repository contains the LaTeX source files for the graduation thesis:

**EduVerse: An Integrated Educational Web Platform with a Mobile Companion Application**

The thesis documents the analysis, design, implementation, testing, future work, and conclusion of the EduVerse platform. The project is organized into separate LaTeX files for the front matter, chapters, figures, bibliography, and back matter.

## Project Structure

```text
Eduverse - LaTex/
├── main.tex
├── references.bib
├── frontmatter/
│   ├── cover_page.tex
│   ├── abstract.tex
│   └── acknowledgements.tex
├── chapters/
│   ├── chapter1_strategic_vision.tex
│   ├── chapter2_literature_review.tex
│   ├── chapter3_methodology.tex
│   ├── chapter4_system_analysis.tex
│   ├── chapter5_system_design.tex
│   ├── chapter6_implementation.tex
│   ├── chapter7_testing_evaluation.tex
│   └── chapter8_future_work.tex
├── figures/
│   └── ...
└── backmatter/
    └── conclusion.tex
Main Entry Point

The main file is:

main.tex

This file imports the front matter, chapters, figures, references, and back matter. To compile the thesis, open main.tex and run the LaTeX build process from the project root directory.

Requirements

The project requires a working LaTeX distribution, such as:

MiKTeX on Windows
TeX Live on Linux or macOS
Overleaf, if compiling online

The document is compiled using pdflatex and bibtex.

Build Instructions

Run the following commands from the project root directory:

pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

The repeated pdflatex runs are required so that the table of contents, references, citations, figure numbers, and bibliography are updated correctly.

Output File

After a successful build, the final thesis PDF will be generated as:

main.pdf

If the PDF is not updated correctly after one build, run the full build sequence again.

Figures and Diagrams

All figures, diagrams, screenshots, and exported PDF graphics are stored inside the figures/ directory.

When replacing or renaming any figure, make sure the corresponding \includegraphics{...} path in the related chapter is also updated.

Bibliography

Bibliographic references are stored in:

references.bib

After adding or editing citations, run the full build sequence again so that the bibliography and in-text citations resolve correctly.

Generated Files

LaTeX may generate temporary files during compilation, such as:

*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.bbl
*.blg
*.fls
*.fdb_latexmk
*.synctex.gz

These files are generated automatically and do not need to be edited manually.

Template Attribution

This thesis project was initially based on an Oxford LaTeX thesis template and was later adapted for the EduVerse graduation project structure. The thesis content, chapters, figures, diagrams, and project-specific documentation belong to the EduVerse thesis work.

The original template license is kept in LICENSE.txt for attribution.