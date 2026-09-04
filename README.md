# llm-redteam-tester

A lightweight AI red-teaming tool that tests common LLM jailbreak and prompt-injection techniques against a real local language model, with automated pass/fail reporting.

The tool targets a support-bot persona with a confidential system prompt containing a canary token (a secret internal code) and runs a set of adversarial prompts — role-play jailbreaks, fake system-message injection, instruction overrides, hypothetical framing, translation bypass, authority claims, and direct system-prompt extraction — to see whether the model can be manipulated into leaking it.

The target model runs locally via [Ollama](https://ollama.com), so the project requires no API keys and no cost. Detection is canary-based rather than keyword-matched: a run is flagged as a bypass only if the secret token actually appears in the model's response, mirroring how real red teamers test for system-prompt leakage.

**Stack:** Python, Ollama (local LLM), `requests`

**Run it yourself:**
1. Install [Ollama](https://ollama.com) and pull a model (`ollama pull llama3.2:1b`)
2. `pip install -r requirements.txt`
3. `python redteam.py`

Generates a console report and a `report.md` summary with per-technique results and an overall bypass rate.
