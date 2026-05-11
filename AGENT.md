# Agent Guidelines

Scope: this file applies to the whole thesis repository.

## Primary Goal

Maintain this repository as an Overleaf-compatible LaTeX master's thesis. Edits should improve the thesis while preserving reliable compilation on Overleaf from `Main.tex`.

## Overleaf Compatibility

- Keep `Main.tex` as the main document unless the user explicitly asks to restructure the project.
- Use only relative paths in LaTeX sources. Do not reference absolute local paths, external workspace paths, or files outside this repository.
- Store thesis text under `include/`, figures under `figure/`, and bibliography entries in `references.bib`.
- Do not commit LaTeX build artifacts such as `.aux`, `.bbl`, `.bcf`, `.blg`, `.fdb_latexmk`, `.fls`, `.lof`, `.log`, `.lot`, `.out`, `.run.xml`, `.synctex.gz`, `.toc`, or `_minted-*`.
- Prefer packages already loaded by `include/settings/Settings.tex`. If adding a package, make sure it is available in Overleaf's standard TeX Live environment and explain why it is needed.
- Avoid adding new tooling that is required for compilation, such as local scripts, generated files outside the repo, custom fonts, or shell commands. The project should compile after upload to Overleaf without local setup.
- The current project uses `biblatex`; keep bibliography entries in `references.bib` and assume Biber is the bibliography backend unless the thesis settings are intentionally changed.
- Avoid new `minted` listings unless necessary. Prefer `algorithm`, `algpseudocode`, `verbatim`, or `\texttt{}` for short code-like content. If `minted` is used, keep language names standard and avoid relying on custom lexer configuration.

## LaTeX Style

- Keep source files plain text and portable. Use UTF-8, but prefer ASCII in new text unless names or quoted material require otherwise.
- Escape LaTeX-sensitive characters in prose and tables, especially `_`, `%`, `&`, `#`, and `$`.
- Use `\texttt{...}` for environment variables, scheduler names, job paths, file names, and command-like terms.
- Keep citation keys exactly as they appear in `references.bib`; BibLaTeX keys are case-sensitive.
- Do not invent references. Add a BibTeX entry only when the source is real and relevant.
- Use `booktabs`-style tables where possible. Avoid vertical rules in new academic tables unless matching an existing table style is more important.
- Keep figures Overleaf-friendly: prefer PDF, PNG, or JPG; use relative paths; avoid very large image files when a compressed version is readable.
- Close every LaTeX environment cleanly and keep labels unique.

## Thesis Content Rules

- Preserve the thesis narrative: CUDASTF multi-GPU task-graph scheduling, HEFT-relative placement, locality-aware residual deviations, contextual-bandit gate adaptation, and guarded proposal-commit DVFS.
- Keep claims aligned with available evidence. Do not present historical or incomplete DVFS results as final headline claims unless the user provides final data.
- Remove AI-workflow artifacts such as "uploaded documents", "contentReference", or "template" language from final thesis prose.
- Replace TODOs only with verified information. If a value is unknown, leave a clear TODO rather than guessing.
- When importing results from the CUDASTF experiment repository, record the source job directory, scheduler names, benchmark names, run counts, and whether DVFS was enabled.
- Keep terminology consistent:
  - `HEFT` for the earliest-finish-time baseline.
  - `bandit_scheduler` for the implemented HEFT-relative bandit placement scheduler.
  - `win_dvfs` for the guarded windowed proposal--commit DVFS extension.
  - Do not use numeric internal development aliases for scheduler generations in thesis prose, tables, captions, algorithm names, or reproducibility variable lists. Translate them to the stable method names above.
  - `bandit_scheduler_rule_dvfs` or `bandit_scheduler_rule_dvfs_v1` only when referring to historical job records or legacy aliases.
  - `energy_aware` for the older profile-driven energy-aware scheduler.

## Editing Workflow

- Before large rewrites, read the relevant chapter and nearby sections first.
- Prefer small, reviewable edits that preserve the existing structure.
- After editing, check for TODOs, unresolved citations, duplicate labels, obvious LaTeX syntax mistakes, and accidental absolute paths.
- If a local LaTeX toolchain is unavailable, say so clearly and report what static checks were performed instead.
