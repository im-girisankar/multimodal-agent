# CLAUDE.md — Multimodal Agent

## Project overview
`multimodal-agent` is a pure-Python agent loop (perceive → reason → act → respond)
with pluggable modalities, a tool registry, and swappable reasoners.

Core package lives in `src/multimodal_agent/`.  Heavy adapters (Whisper, pyttsx3,
Pillow, Anthropic) are in `src/multimodal_agent/adapters/` and are **never imported
at the top level** — always lazy-import inside methods/functions.

## Running locally
```bash
pip install -e ".[dev]"    # core + pytest + ruff
pytest                     # all tests (offline, no GPU/keys)
ruff check src tests       # lint
ruff format src tests      # format
mma run "hello"            # CLI smoke test
```

## Testing rules
- Tests live in `tests/`.
- All tests must pass with only `pytest` + `ruff` installed (no extras).
- Never import `whisper`, `pyttsx3`, `PIL`, or `anthropic` in tests or package
  top-level modules.
- Use `MockReasoner(script=[...])` to control agent behaviour deterministically
  in tests.

## Lint / format
- ruff, line-length 100, rules E F I UP B, ignore E501.
- Run `ruff check --fix src tests` before committing.

## Adding a new tool
1. Write a plain Python function in `src/multimodal_agent/tools.py`.
2. Register it: `default_registry.register("name", fn)`.
3. Add a test in `tests/test_tools.py`.

## Adding a new modality or sink adapter
1. Create `src/multimodal_agent/adapters/<name>.py`.
2. Lazy-import all heavy libraries inside methods.
3. Raise a clear `ImportError` with install instructions when the extra is missing.
4. Do NOT exercise the adapter in CI tests.

## Architecture notes
- `types.py` — data classes only; zero imports from this package.
- `modality.py` / `output.py` — protocols + lightweight stubs; no heavy deps.
- `reasoner.py` — MockReasoner is heuristic + scriptable; LLMReasoner is in adapters/.
- `agent.py` — orchestrates the loop; catches all ToolError so the loop never crashes.
- `cli.py` — thin argparse wrapper; testable by capturing stdout.
