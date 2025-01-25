# altotech_podcast/ui/prompts.py
from typing import Any

from rich.prompt import Prompt, Confirm

class PodcastPrompts:
    """Handles user input prompts during the podcast."""
    
    @staticmethod
    def get_audience_question() -> str | None:
        """Get an audience question if available."""
        if Confirm.ask("\n👥 Audience question?", default=False):
            return Prompt.ask("Enter question")
        return None
    
    @staticmethod
    def should_end_podcast() -> bool:
        """Check if we should end the podcast completely."""
        return Confirm.ask(
            "\nWould you like to end the podcast?",
            default=False
        )

    @staticmethod
    def should_continue() -> bool:
        """Check if we should move to the next topic."""
        return Confirm.ask(
            "\nMove to next topic?",
            default=True
        )
    
    @staticmethod
    def get_choice(
        options: list[str],
        prompt: str = "Choose an option",
        default: str | None = None
    ) -> str:
        """Get a choice from a list of options."""
        return Prompt.ask(
            prompt,
            choices=options,
            default=default or options[0]
        )
    
    @staticmethod
    def get_value(
        prompt: str,
        type_: type = str,
        default: Any | None = None,
        **kwargs: Any
    ) -> Any:
        """Get a typed value from the user."""
        return Prompt.ask(
            prompt,
            default=default,
            type=type_,
            **kwargs
        )