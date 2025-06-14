def parse_dialog_list(row, recipe):
    dialog_field = recipe.get("dialog_field", "dialog")
    dialog = row.get(dialog_field, [])
    if not dialog:
        return []

    role_map = {
        "user": "User",
        "assistant": "Bot",
        "Seeker": "User",
        "Supporter": "Bot",
    }

    utterances = build_utterances(dialog, role_map)
    return build_examples(utterances)

def build_examples(utterances):
    examples = []
    for i in range(1, len(utterances)):
        input_text = "\n".join(utterances[:i])
        target_text = utterances[i].split(": ", 1)[-1]
        examples.append({"input": input_text, "target": target_text})
    return examples

def build_utterances(dialog, role_map):
    utterances = []
    for idx, turn in enumerate(dialog):
        speaker = extract_speaker(turn, idx, role_map)
        content = extract_content(turn)
        if content:
            utterances.append(f"{speaker}: {content}")
    return utterances

def extract_speaker(turn, idx, role_map):
    if isinstance(turn, dict):
        speaker_raw = turn.get("role") or turn.get("speaker") or turn.get("sender")
        speaker = role_map.get(speaker_raw, "Speaker")
        if not speaker:
            speaker = "User" if idx % 2 == 0 else "Bot"
    else:
        speaker = "User" if idx % 2 == 0 else "Bot"
    return speaker

def extract_content(turn):
    if isinstance(turn, dict):
        return turn.get("content", "").strip()
    else:
        return str(turn).strip()
