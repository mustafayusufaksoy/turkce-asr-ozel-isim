"""Optional selector that uses the Claude API (pip install "turkce-asr-ozel-isim[claude]")."""


def claude_selector(api_key=None, model="claude-haiku-5-5"):
    """Return an ask() function for select_candidates. Reads ANTHROPIC_API_KEY by default."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    def ask(system, text):
        response = client.messages.create(model=model, max_tokens=4000, system=system,
                                          messages=[{"role": "user", "content": text}])
        if response.stop_reason != "end_turn":
            raise RuntimeError(f"incomplete model response: stop_reason={response.stop_reason!r}")
        return "".join(block.text for block in response.content if block.type == "text")
    return ask
