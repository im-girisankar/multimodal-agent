# multimodal-agent

A hands-free, see-and-act AI assistant that loops through
**perceive → reason → act → respond** using pluggable modalities, a tool
registry, and a swappable reasoner.

> **Status**: Milestone 1 complete (text stub + mock reasoner + tool dispatch).
> Real STT/TTS/vision adapters and the LLM reasoner are wired but untested in CI —
> they require the optional extras listed below and appropriate hardware/API keys.

---

## Architecture

```
TextModality / WhisperModality / VisionModality
          │  (capture → text)
          ▼
       Agent.run(text)
          │
          ├─ perceive ── builds Context
          │
          ├─ reason  ── MockReasoner | LLMReasoner → Action
          │
          ├─ act     ── ToolRegistry.dispatch → Observation → back to reason
          │                 (calculator, clock, …)
          │
          └─ respond ── TextSink | PrintSink | TTSSink
```

## Milestones

| # | Status | Description |
|---|--------|-------------|
| M1 | ✅ Done | Text stub, MockReasoner, tool registry (calc + clock), TextSink, CLI |
| M2 | 🔲 Planned | Whisper STT + pyttsx3 TTS adapters wired into the live loop |
| M3 | 🔲 Planned | Vision modality (Pillow + optional caption model) |
| M4 | 🔲 Planned | LLMReasoner (Anthropic) with structured tool-use response parsing |

---

## Quick start (offline demo)

```bash
pip install -e ".[dev]"
pytest                     # 20+ tests, no network/keys/GPU required
mma run "hello"            # text → mock reasoning → final response
mma run "calc 3 + 4"       # triggers the calculator tool
mma run "what time is it?" # triggers the clock tool
mma tools                  # list registered tools
```

## Optional extras

| Extra | Installs | Enables |
|-------|----------|---------|
| `audio` | `openai-whisper`, `pyttsx3` | WhisperModality, TTSSink |
| `vision` | `pillow` | VisionModality |
| `llm` | `anthropic>=0.39` | LLMReasoner |
| `dev` | `pytest>=7`, `ruff>=0.4` | Test + lint |

```bash
pip install -e ".[audio,vision,llm]"
```

> **Note**: Real STT (Whisper) requires ffmpeg and a GPU for fast inference.
> TTS (pyttsx3) is synchronous and may be slow on first use.
> CI only exercises the pure-Python stubs — heavy adapters are **not** run.

## Project layout

```
src/multimodal_agent/
├── __init__.py
├── types.py        # Action, ToolCall, FinalResponse, Context
├── modality.py     # Modality protocol + TextModality stub
├── reasoner.py     # Reasoner protocol + MockReasoner
├── tools.py        # ToolRegistry + calculator + clock
├── output.py       # OutputSink + TextSink + PrintSink
├── agent.py        # Agent (the main loop)
├── cli.py          # `mma` CLI
└── adapters/
    ├── stt.py      # WhisperModality (lazy import)
    ├── vision.py   # VisionModality  (lazy import)
    ├── tts.py      # TTSSink         (lazy import)
    └── llm.py      # LLMReasoner     (lazy import)
tests/
├── test_modality.py
├── test_tools.py
├── test_output.py
├── test_agent.py
└── test_cli.py
```

## License

MIT © 2026 Girisankar G
