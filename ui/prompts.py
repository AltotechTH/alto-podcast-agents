# altotech_podcast/ui/prompts.py
from typing import Any

from rich.prompt import Prompt, Confirm
from pydantic_ai import Agent
from context.company import CompanyContext
from context.topics import get_topic_prompt
from models.enums import TopicArea

class PodcastPrompts:
    """Handles user input prompts during the podcast."""
    
    def __init__(self):
        """Initialize the LLM agent for decision making."""
        self.agent = Agent(
            "openai:gpt-3.5-turbo",  # Using a smaller model for simple decisions
            system_prompt="""You are a podcast producer helping to manage the flow of conversation.
Your job is to analyze the recent conversation and company context to decide if:
1. The current topic has been sufficiently covered and it's time to move on
2. The podcast should end because all key points have been discussed thoroughly
Base your decisions on:
- The depth and completeness of the discussion
- Whether key points have been addressed
- The natural flow of conversation
- Whether there are still interesting angles to explore
Keep the podcast engaging but concise."""
        )
        self.company = CompanyContext()
    
    @staticmethod
    def get_audience_question() -> str | None:
        """Get an audience question if available."""
        if Confirm.ask("\n👥 Audience question?", default=False):
            return Prompt.ask("Enter question")
        return None

    async def should_end_podcast(self, topic: TopicArea, recent_exchanges: list[str]) -> bool:
        """Determine if we should end the podcast based on topic coverage."""
        # The podcast should only end when all topics have been covered
        return False  # This will be handled by the main loop when all topics are done

    async def should_continue(self, topic: TopicArea, recent_exchanges: list[str]) -> bool:
        """Use LLM to decide if we should move to the next topic."""
        topic_info = get_topic_prompt(topic)
        company_context = self.company.format_for_prompt()
        
        prompt = f"""Company Context:
{company_context}

Current Topic Information:
Main Topic: {topic.display_name}
Context: {topic_info.context}
Key Questions:
{chr(10).join(f"- {q}" for q in (topic_info.suggested_questions or []))}

Recent conversation:
{chr(10).join(recent_exchanges)}

Should we move to the next topic? Consider carefully and be conservative in your decision.
The discussion should thoroughly explore the current topic before moving on.

Specific requirements to move on:
1. Have ALL key questions been addressed in detail?
2. Has the discussion explored multiple perspectives and implications?
3. Have we covered both high-level strategy and specific implementation details?
4. Has there been a natural conclusion to the current discussion thread?
5. Have we discussed concrete examples and applications?

Only respond 'yes' if requirements reasonably are met. Otherwise respond 'no'.
Include a brief explanation focusing on what aspects still need more discussion."""

        result = await self.agent.run(prompt)
        decision = result.data.lower().strip().startswith('yes')
        return decision
    
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