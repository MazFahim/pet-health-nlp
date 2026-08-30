# Contributing

Thanks for your interest in this project! It's a small, solo-maintained tool,
so contributions are welcome but the process is kept lightweight.

## Reporting issues

If you find a bug, a misclassification pattern, or have a suggestion, please
open a [GitHub Issue](../../issues) describing:
- What you expected to happen
- What actually happened
- A minimal example input, if relevant

## Suggesting improvements

Ideas for new features, additional condition categories, or prompt
improvements are welcome — open an issue to discuss before submitting a
large pull request, so we can make sure it fits the project's scope.

## Submitting a pull request

1. Fork the repository and create a new branch for your change.
2. Make your changes, keeping them focused and easy to review.
3. If you change `extractor.py`, please run the existing tests
   (`python -m unittest tests.test_extractor -v`) and add a new test if
   you're adding behavior.
4. Open a pull request with a short description of what changed and why.

## Known limitations

Before reporting a misclassification, it may already be a documented,
expected limitation — see the [Limitations](README.md#limitations) section
of the README and `findings.md` for details on known failure patterns.
