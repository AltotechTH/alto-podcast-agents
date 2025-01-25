# altotech_podcast/models/state.py
from dataclasses import dataclass, field
from datetime import datetime

from pydantic_ai.messages import ModelMessage

from .enums import TopicArea
from .dialogue import DialogueContent

@dataclass
class PodcastState:
    """State maintained throughout the podcast conversation."""
    current_topic: TopicArea
    start_time: datetime = field(default_factory=datetime.now)
    dialogue_history: list[DialogueContent] = field(default_factory=list)
    audience_questions: list[str] = field(default_factory=list)
    host_messages: list[ModelMessage] = field(default_factory=list)
    guest_messages: list[ModelMessage] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        """Returns the current duration of the podcast in minutes."""
        return (datetime.now() - self.start_time).total_seconds() / 60
    
    @property
    def exchange_count(self) -> int:
        """Returns the total number of dialogue exchanges."""
        return len(self.dialogue_history)
    
    def add_dialogue(self, content: DialogueContent) -> None:
        """Add a new dialogue exchange to the history."""
        self.dialogue_history.append(content)
    
    def add_audience_question(self, question: str) -> None:
        """Add a new audience question."""
        self.audience_questions.append(question)
    
    def get_last_exchange(self, role: str | None = None) -> DialogueContent | None:
        """Get the last dialogue exchange, optionally filtered by role."""
        if role is None:
            return self.dialogue_history[-1] if self.dialogue_history else None
        
        for exchange in reversed(self.dialogue_history):
            if exchange["role"] == role:
                return exchange
        return None

    def get_current_topic_exchanges(self, limit: int = 5) -> list[str]:
        """Get the most recent dialogue exchanges for the current topic."""
        recent_exchanges = []
        for exchange in reversed(self.dialogue_history[-limit:]):
            role = exchange["role"]
            content = exchange["content"]
            recent_exchanges.insert(0, f"{role.title()}: {content}")
        return recent_exchanges