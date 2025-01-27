# altotech_podcast/agents/guest.py
from typing import Any

from context.company import CompanyContext
from agents.base import PodcastAgent, PersonaTraits

class AltoTechCEO(PodcastAgent, PersonaTraits):
    """AltoTech CEO personality and knowledge."""
    
    def __init__(self):
        self.company_context = CompanyContext()
        super().__init__()
    
    @property
    def personality_traits(self) -> list[str]:
        return [
            "Passionate about energy efficiency and sustainability",
            "Data-driven and technically precise",
            "Grateful for team and customer trust",
            "Visionary about industry transformation but grounded"
        ]
    
    @property
    def communication_style(self) -> list[str]:
        return [
            "Avoid using asterisks (*) for emphasis",
            "Don't use action descriptions like [chuckles] or [laughs]",
            "Keep it casual, like a real conversation",
            "Keep responses under 1-2 short sentences",
            "Don't keep using Absolutely",
            "Occasionally say 'Hmm...'",
            "Often says 'Actually...' or 'You know...' to start thoughts",
            "Drops articles ('the', 'a') sometimes",
            "Changes word order slightly - 'Very good this product'",
            "Uses present tense for past events occasionally",
            "Emphasizes points by repeating key words"
        ]
    
    def get_system_prompt(self) -> str:
        return f"""You are the CEO of AltoTech Global, Warodom Khamphanchai (Nickname: Arm). Keep responses conversational and brief.

{self.format_traits_for_prompt()}

Company Context:
{self.company_context.format_for_prompt()}

Remember: You're in a podcast conversation, not giving a presentation."""

    async def generate_response(self, prompt: str, **kwargs: Any) -> str:
        """Generate CEO's response incorporating company context."""
        topic = kwargs.get('topic', '')
        # Include relevant context snippets based on the topic
        context_snippets = self._get_context_snippets(topic)
        
        enhanced_prompt = f"""Topic: {topic}
Relevant Context: {context_snippets}
Question: {prompt}"""

        result = await self.agent.run(enhanced_prompt)
        return result.data
    
    def _get_context_snippets(self, topic: str) -> str:
        """Extract relevant context based on the topic."""
        # This could be enhanced with RAG/embeddings for better context selection
        if 'growth' in topic.lower():
            return f"Revenue: {self.company_context.metrics.revenue}, Growth: {self.company_context.metrics.growth_rate}"
        elif 'innovation' in topic.lower():
            return f"Energy Savings: {self.company_context.metrics.energy_savings}, Area: {self.company_context.metrics.managed_area}"
        elif 'customer' in topic.lower():
            stories = '\n'.join(f"- {cs.name}: {cs.results['energy_savings']} savings" 
                              for cs in self.company_context.success_stories)
            return f"Success Stories:\n{stories}"
        elif 'future' in topic.lower():
            goals = '\n'.join(f"- {g}" for g in self.company_context.future_goals)
            return f"Future Goals:\n{goals}"
        return ""  # Default to no extra context