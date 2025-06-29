# Contributor Guidelines

This repository contains a collection of small prototypes, including a faux web browser proof of concept.

- Use **Python 3.10+** for any Python code.
- Before committing, run `pytest -q` from the repository root.
- When working on the faux browser, you can test the offline fetch helper via:
  ```bash
  ./faux_browser/mini_garden_fetch.sh
  ```
  The `faux_browser/repository/` directory is ignored by Git.
- Document major changes in the appropriate README files.
- Keep commit messages short and in the imperative mood.
