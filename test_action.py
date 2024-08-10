from aijson import register_action

@register_action
def test_action(name: str) -> str:
    return name.upper()