"""Emptying a commented section must still leave a parseable config (#154436).

`config migrate` deletes keys the managed scope owns. When that empties a section that also
carries comment lines, the round-trip writer used to emit the empty mapping as a column-0
``{}`` beneath those comments, and the next parse rejected the whole file.
"""

import hermes_yaml as yaml
from utils import atomic_roundtrip_yaml_update

SOURCE = (
    "skills:\n"
    "  # Nudge the agent to create skills.\n"
    "  creation_nudge_interval: 5\n"
    "\n"
    "  # Set to 0 to disable.\n"
    "agent:\n"
    "  max_turns: 5\n"
)


def test_removing_the_last_key_of_a_commented_section_keeps_the_file_parseable(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text(SOURCE, encoding="utf-8")

    atomic_roundtrip_yaml_update(path, "skills.creation_nudge_interval", None)

    content = path.read_text(encoding="utf-8")
    assert yaml.safe_load(content) == {"skills": {}, "agent": {"max_turns": 5}}
