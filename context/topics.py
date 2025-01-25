# altotech_podcast/context/topics.py
from typing import NamedTuple

from models.enums import TopicArea

class TopicPrompt(NamedTuple):
    """Structure for topic prompts and context."""
    main_prompt: str
    context: str | None = None
    suggested_questions: list[str] | None = None

# Mapping of topics to their prompts and context
TOPIC_PROMPTS: dict[TopicArea, TopicPrompt] = {
    TopicArea.COMPANY_GROWTH: TopicPrompt(
        "Let's talk about AltoTech's growth journey and current success metrics.",
        context="Focus on the rapid revenue growth and expansion of managed area.",
        suggested_questions=[
            "What were the key inflection points in your growth?",
            "How did you achieve such impressive YoY growth?",
            "What metrics are you most proud of?"
        ]
    ),
    
    TopicArea.PRODUCT_INNOVATION: TopicPrompt(
        "Tell us about your AI-powered HVAC optimization technology.",
        context="Technical discussion about AI/ML implementation and energy savings.",
        suggested_questions=[
            "How does your AI actually optimize HVAC systems?",
            "What makes your solution different from traditional systems?",
            "Can you share some specifics about your energy saving algorithms?"
        ]
    ),
    
    TopicArea.CUSTOMER_SUCCESS: TopicPrompt(
        "Share some success stories from your premium property clients.",
        context="Focus on specific examples and testimonials.",
        suggested_questions=[
            "What's your most impressive customer success story?",
            "How do you measure and verify the energy savings?",
            "What feedback do you get from building operators?"
        ]
    ),
    
    TopicArea.MARKET_EXPANSION: TopicPrompt(
        "Your expansion into new markets - especially Singapore. How's that going?",
        context="Discussion of international expansion and market challenges.",
        suggested_questions=[
            "What's different about each market you operate in?",
            "How do you handle different building types and climates?",
            "What's your strategy for entering new markets?"
        ]
    ),
    
    TopicArea.CHALLENGES: TopicPrompt(
        "What challenges have you faced scaling a deep-tech startup in Southeast Asia?",
        context="Open discussion about technical and business challenges.",
        suggested_questions=[
            "What's been your biggest technical challenge?",
            "How do you handle skepticism from potential clients?",
            "What surprised you most about scaling the business?"
        ]
    ),
    
    TopicArea.FUTURE_VISION: TopicPrompt(
        "With your Series A raise, what's your vision for the next 5 years?",
        context="Forward-looking discussion about growth plans and innovation.",
        suggested_questions=[
            "How will you use the Series A funding?",
            "What new features or products are you planning?",
            "Where do you see the biggest opportunities?"
        ]
    )
}

def get_topic_prompt(topic: TopicArea) -> TopicPrompt:
    """Get the prompt and context for a given topic."""
    return TOPIC_PROMPTS[topic]