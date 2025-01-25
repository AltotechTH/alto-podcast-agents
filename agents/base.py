# altotech_podcast/agents/base.py
from abc import ABC, abstractmethod
from typing import Any
import os
from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

class PodcastAgent(ABC):
    """Base class for podcast agents with common functionality."""
    
    def __init__(self, use_mini_model: bool = False):
        model = os.getenv('AZURE_OPENAI_REASONING_MODEL') if use_mini_model else os.getenv('AZURE_OPENAI_REASONING_MODEL')
        azure_client = AsyncAzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        )
        openai_model = OpenAIModel(model, openai_client=azure_client)
        self.agent = Agent(
            openai_model,
            system_prompt=self.get_system_prompt()
        )
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs: Any) -> str:
        """Generate a response to the given prompt."""
        pass

class PersonaTraits:
    """Mixin for agent personality traits."""
    
    @property
    @abstractmethod
    def personality_traits(self) -> list[str]:
        """Return list of personality traits for the agent."""
        pass
    
    @property
    @abstractmethod
    def communication_style(self) -> list[str]:
        """Return list of communication style guidelines."""
        pass
    
    def format_traits_for_prompt(self) -> str:
        """Format traits for inclusion in system prompt."""
        return f"""Personality Traits:
{chr(10).join(f"- {t}" for t in self.personality_traits)}

Communication Style:
{chr(10).join(f"- {s}" for s in self.communication_style)}"""