# EduVerse Thesis Documentation

This repository contains the LaTeX source files for the graduation thesis:

**EduVerse: An Integrated Educational Web Platform with a Mobile Companion Application**

The thesis documents the academic analysis, design, implementation, testing, future work, and conclusion of the EduVerse platform. The project is organized into separate LaTeX files for the front matter, chapters, figures, bibliography, and back matter.

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
│   ├── activity_diagrams/
│   ├── diagrams/
│   └── ...
├── backmatter/
│   └── conclusion.tex
├── LICENSE.txt
└── README.md
```

## Main Entry Point

The main LaTeX entry file is:

```text
main.tex
```

This file controls the full thesis build. It includes the front matter, chapters, figures, bibliography, and back matter. To compile the thesis correctly, run the build commands from the root directory of the project.

## Requirements

To compile the thesis locally, install a working LaTeX distribution such as:

- MiKTeX on Windows
- TeX Live on Linux or macOS
- Overleaf, if compiling online

The thesis is compiled using `pdflatex` and `bibtex`.

## Build Instructions

Run the following commands from the project root directory:

```bash
pdflatex -interaction=nonstopmode -synctex=1 main.tex
bibtex main
pdflatex -interaction=nonstopmode -synctex=1 main.tex
pdflatex -interaction=nonstopmode -synctex=1 main.tex
```

The repeated `pdflatex` runs are required so that the table of contents, citations, bibliography, figure numbers, table numbers, and cross-references are updated correctly.

## Output File

After a successful build, the final thesis PDF will be generated as:

```text
main.pdf
```

If the PDF does not update correctly after one build, run the full build sequence again.

## Figures and Diagrams

All figures, diagrams, screenshots, exported PDF graphics, and supporting figure files are stored inside the `figures/` directory.

When replacing or renaming a figure, make sure the related `\includegraphics{...}` path in the corresponding chapter is also updated.

## Bibliography

Bibliographic references are stored in:

```text
references.bib
```

After adding, removing, or editing citations, run the full build sequence again so that the bibliography and in-text citations resolve correctly.

## Generated Files

LaTeX may generate temporary files during compilation, such as:

```text
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
```

These files are generated automatically and do not need to be edited manually. They can be safely deleted because LaTeX will recreate them during the next build.

## Notes About the Final PDF

The generated `main.pdf` file is the final compiled thesis output. It may be excluded from version control using `.gitignore`, but it should be shared when submitting or sending the final thesis for review.

## Template Attribution

This thesis project was initially based on an Oxford LaTeX thesis template and was later adapted for the EduVerse graduation project structure.

The thesis content, chapters, diagrams, figures, and documentation text are maintained for the EduVerse graduation project, not as a generic Oxford template distribution.

The original template license is kept in `LICENSE.txt` for attribution.