# altotech_podcast/models/enums.py
from enum import Enum
from typing import Literal
from typing_extensions import TypeAlias

# Role types
Role: TypeAlias = Literal["host", "guest"]
DialogueType: TypeAlias = Literal["question", "response", "transition", "audience_response"]

class TopicArea(str, Enum):
    """Core topic areas for the podcast conversation."""
    COMPANY_GROWTH = "company_growth"
    PRODUCT_INNOVATION = "product_innovation"
    CUSTOMER_SUCCESS = "customer_success"
    MARKET_EXPANSION = "market_expansion"
    CHALLENGES = "challenges"
    FUTURE_VISION = "future_vision"
    
    @property
    def display_name(self) -> str:
        """Returns a human-readable version of the topic name."""
        return self.value.replace('_', ' ').title()