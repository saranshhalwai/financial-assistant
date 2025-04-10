# Financial Trading Assistant

```bash
financial-assistant/
│
├── agents/                   # Agent logic (LLM wrappers, analysis)
│   ├── technical.py
│   ├── fundamental.py
│   └── __init__.py
│
├── core/                     # Core logic (decision-making, reasoning)
│   ├── decision_engine.py
│   ├── forecasting.py
│   └── __init__.py
│
├── utils/                    # Utilities (API handlers, indicators, helpers)
│   ├── data_fetch.py
│   ├── indicators.py
│   └── logger.py
│
├── config/                   # API keys, model configs, constants
│   └── settings.py
│
├── app.py                    # Main runner script
├── requirements.txt          # All the cursed packages
├── README.md                 # Your gospel
└── .env                      # For sensitive configs (don’t push to GitHub)
```
