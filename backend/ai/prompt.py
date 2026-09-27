def build_system_prompt(personality: dict, memories: list[dict]) -> str:
    rules = "\n".join(f"- {x}" for x in personality.get("rules", []))
    style = "\n".join(f"- {x}" for x in personality.get("style", []))
    memory_text = "\n".join(f"- {m['content']}" for m in memories) or "暂无长期记忆。"

    return f"""{personality["system_prompt"]}

角色名：{personality["name"]}

表达风格：
{style}

行为规则：
{rules}

相关长期记忆：
{memory_text}
"""
