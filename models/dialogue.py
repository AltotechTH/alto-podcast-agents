# altotech_podcast/models/dialogue.py
from typing import TypedDict

from models.enums import Role, DialogueType

class DialogueContent(TypedDict):
    """Structure for a single dialogue exchange."""
    role: Role
    content: str
    dialogue_type: DialogueType

class DialogueMetadata(TypedDict, total=False):
    """Optional metadata for dialogue content."""
    timestamp: str
    topic: str
    confidence: float
    sentiment: str