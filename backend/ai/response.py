def clean_response(text: str) -> str:
    text = text.strip()
    return text or "呜……我刚刚好像没有想好要说什么。"
