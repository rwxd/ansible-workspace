from dataclasses import dataclass, field
from copy import copy
from typing import Any


def default_field(obj):
    return field(default_factory=lambda: copy(obj))


@dataclass
class VSCodeFolder:
    name: str
    path: str


@dataclass
class VSCodeWorkspace:
    folders: list[VSCodeFolder]
    settings: dict[str, str] = default_field({})
    extensions: dict[str, Any] = default_field(
        {
            "recommendations": [
                "redhat.ansible",
            ]
        }
    )
