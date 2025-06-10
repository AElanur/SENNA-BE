import re

def parse_regex(row, recipe):
    text = row.get('text', '')
    match = re.match(recipe["pattern"], text, re.DOTALL)
    if match:
        input_text = match.group(1).strip()
        target_text = match.group(2).strip()

        if recipe.get("add_speaker_tags", False):
            input_text = f"User: {input_text}"
            target_text = f"{target_text}"

        return [{
            "input": input_text,
            "target": target_text
        }]
    return []

def parse_dialog_list(row, recipe):
    dialog_field = recipe.get("dialog_field", "dialog")
    dialog = row.get(dialog_field, [])
    if not dialog:
        return []

    role_map = {
        "user": "User",
        "assistant": "Bot",
        "Seeker": "User",
        "Supporter": "Bot"
    }

    utterances = []
    for idx, turn in enumerate(dialog):
        if isinstance(turn, dict):
            speaker_raw = turn.get("role") or turn.get("speaker") or turn.get("sender")
            speaker = role_map.get(speaker_raw, f"Speaker")
            if not speaker:
                speaker = "User" if idx % 2 == 0 else "Bot"
            content = turn.get("content", "").strip()
        else:
            speaker = "User" if idx % 2 == 0 else "Bot"
            content = str(turn).strip()

        if content:
            utterances.append(f"{speaker}: {content}")

    examples = []
    for i in range(1, len(utterances)):
        input_text = "\n".join(utterances[:i])
        target_text = utterances[i].split(": ", 1)[-1]
        examples.append({"input": input_text, "target": target_text})

    return examples

def parse_classification(row, recipe):
    fields = recipe.get("fields", [])
    if not all(field in row for field in fields):
        return []
    input_text = str(row[fields[0]]).strip()
    target_text = str(row[fields[1]]).strip()
    return [{
        "input": input_text,
        "target": target_text
    }]
