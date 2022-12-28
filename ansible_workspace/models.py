from dataclasses import dataclass
from typing import Optional


@dataclass
class AnsibleRole:
    name: str
    src: str
    scm: str
    version: Optional[str] = None
