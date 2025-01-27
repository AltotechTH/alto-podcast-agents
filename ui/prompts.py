# altotech_podcast/ui/prompts.py
import json
from typing import Any
import os
from dotenv import load_dotenv
from rich.prompt import Prompt, Confirm
from pydantic_ai import Agent
from openai import AsyncAzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
from context.company import CompanyContext
from context.topics import get_topic_prompt
from models.enums import TopicArea

load_dotenv()

class PodcastPrompts:
    """Handles user input prompts during the podcast."""
    
    def __init__(self):
        """Initialize the LLM agent for decision making."""
        model = os.getenv('AZURE_OPENAI_MINI_MODEL')
        azure_client = AsyncAzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        )
        openai_model = OpenAIModel(model, openai_client=azure_client)
        
        self.latest_answered_q_index = 0

        self.agent = Agent(
            openai_model,
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
        self.last_processed_timestamp = None
        
    def clear_submissions(self) -> None:
        """Clear all submissions from the submissions.json file."""
        try:
            with open('qr/submissions.json', 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Error clearing submissions: {e}")
    
    def get_audience_question(self) -> str | None:
        """Get an audience question from submissions.json if available."""
        try:
            # Read submissions from file
            with open('qr/submissions.json', 'r') as f:
                submissions = json.loads(f.read())
                
            if submissions:
                selected_index = self.latest_answered_q_index
                if selected_index >= len(submissions):
                    return None
                
                submission = submissions[selected_index]
                self.latest_answered_q_index = selected_index + 1
                return f"{submission['name']} asks: {submission['question']}"
            else:
                return None
            
            # Filter and sort submissions by timestamp
            new_submissions = [
                s for s in submissions 
                if (self.last_processed_timestamp is None or 
                    s['timestamp'] > self.last_processed_timestamp)
            ]
            
            if not new_submissions:
                return None
                
            # Get the oldest unprocessed submission
            submission = sorted(new_submissions, key=lambda x: x['timestamp'])[0]
            self.last_processed_timestamp = submission['timestamp']
            
            # Format the question with the submitter's name
            return f"{submission['name']} asks: {submission['question']}"
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading submissions: {e}")
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

Should we move to the next topic? Consider:
1. Has this topic been sufficiently covered given the context?
2. Have we addressed the key questions for this topic?
3. Are there still important points to discuss?
4. Is this a natural point to transition?

We should move on if they are sufficiently met.
Respond with either 'yes' or 'no' and a brief explanation."""

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