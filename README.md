# EduVerse Thesis Documentation

This repository contains the LaTeX source for the thesis:

**EduVerse: An Integrated Educational Web Platform with a Mobile Companion Application**

The project documents the academic analysis, design, implementation, testing, and conclusion chapters for the EduVerse platform, together with the front matter, figures, references, and supporting thesis assets required to build the final PDF.

## Repository Structure

- `main.tex` — main thesis entry point.
- `frontmatter/` — cover page, abstract, acknowledgements, and other opening sections.
- `chapters/` — numbered thesis chapters.
- `figures/` — diagrams, screenshots, ERD assets, and supporting figure sources.
- `backmatter/` — conclusion and closing sections.
- `references.bib` — bibliography entries used by the thesis.
- `OxfordTeXThesis.cls` — adapted thesis class used to format the document.

## Compilation

Compile the thesis with the standard LaTeX and BibTeX sequence:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If the local toolchain is configured for XeLaTeX or an automated build script, keep the same multi-pass bibliography workflow so that references, contents pages, figure numbers, and table numbers update correctly.

## Figures and Screenshots

- Figures are stored under `figures/` and may include PDF diagrams, exported screenshots, and supporting LaTeX figure sources.
- Screenshot paths and filenames should remain stable unless the thesis text is updated to match.
- When replacing a figure, preserve readability, caption relevance, and the intended chapter context.

## References

- Bibliographic entries are maintained in `references.bib`.
- After adding or editing citations, rerun the full compile sequence so that the bibliography and in-text references resolve correctly.
- Avoid removing bibliography entries unless they are clearly unused or replaced.

## Template Attribution

This thesis project uses an adapted `OxfordTeXThesis` class and template as its LaTeX formatting base. The repository content, chapter structure, figures, and documentation text are maintained for the EduVerse thesis project rather than as a generic upstream template distribution.
