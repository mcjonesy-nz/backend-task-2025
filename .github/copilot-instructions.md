# Copilot / AI Agent Instructions

Purpose: concise, actionable guidance to help an AI coding agent be productive in this repository.

- **Project type:** Serverless text-analysis microservice (Python + AWS Lambda expected).
- **Key files:** `README.md` (service spec & input/output formats), `data/` (sample JSON inputs).

Quick orientation
- The service accepts JSON with two formats: Standalone and Comparative (see `README.md`).
- Input sentences include `id` values; an `id` can appear multiple times in input but should appear at most once per resulting cluster.
- Expected output is JSON with top-level `clusters` and fields like `title`, `sentiment`, `sentences`, and `keyInsights`.

Architecture summary (what to assume from repo)
- Design: API Gateway -> AWS Lambda (Python) -> preprocessing -> clustering -> sentiment -> JSON response.
- Integration points to mention in changes: AWS Lambda handler, API Gateway mapping, optional S3 for artifacts, and IaC (SAM/Serverless/CDK).

Developer workflows & checks (discoverable / reproducible)
- There are no build/test scripts in the repo. Use these quick checks while working:
  - Validate sample JSONs: `python -m json.tool data/input_example.json`
  - When adding Python code, include a minimal `requirements.txt` or `pyproject.toml` and unit tests under `tests/`.
  - When writing tests, use unittest over pytest for compatibility
  - Package for lambda locally with `zip` or use AWS SAM/Serverless Framework for deployment.
  - When testing locally run the `python3 -m project.app` from the root directory
  - Use linting tools like `flake8` or `pylint` for Python code quality checks.
  - When logging use `logger.info()` or similar instead of print statements.

Test runner (recommended)
- A small test runner is provided at `scripts/run_tests.py` which ensures the repo root
  is on `sys.path` and runs `unittest` discovery. Run tests with:

  ```bash
  python3 scripts/run_tests.py
  ```

Alternatively run discovery directly from the repo root:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
```

Project-specific conventions & constraints
- Language preference: Python (README explicitly requests Python).
- Keep changes minimal and self-contained: prefer adding a small Lambda handler and a test harness that uses `data/*.json`.
- Preserve the exact output JSON schema from `README.md` (field names and nesting matter for graders/tests).
- Ensure dedup semantics: allow same input `id` to be in multiple clusters overall, but only once per cluster.

What to look for when editing or adding code
- Data Models exist in `models.py` for Payload and Response structures; use them to enforce typing.
- Reference sample inputs in `data/` for unit tests and examples.
- When implementing clustering, include a deterministic fallback (e.g., simple TF-IDF + cosine) so results are reproducible in tests.
- Document any model/AI usage in the repo root (README or a short `AI_USAGE.md`) as requested by the spec.

If merging existing instructions
- If a `.github/copilot-instructions.md` already exists, merge by keeping any repository-specific examples and updating the “Developer workflows” section to match `README.md` requirements.

Notes for reviewers/agents
- Focus on delivering a minimal working Lambda and demonstrable tests using `data/*` sample payloads.
- Do not introduce heavy infra changes without an accompanying minimal deployment guide (commands or SAM template snippet).

Next step: ask reviewer what additional CI, test, or deployment commands they expect (SAM/Serverless/CDK).
