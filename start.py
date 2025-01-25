# altotech_podcast/main.py
import asyncio
from typing import List, Dict

from agents.host import ElonMuskHost
from agents.guest import AltoTechCEO
from models.state import PodcastState
from models.enums import TopicArea
from ui.console import PodcastConsole
from ui.prompts import PodcastPrompts

async def run_podcast():
    # Initialize components
    console = PodcastConsole()
    prompts = PodcastPrompts()
    host = ElonMuskHost()
    guest = AltoTechCEO()
    
    # Start podcast
    prompts.clear_submissions()
    console.print_header()
    
    # Opening
    opening = await host.generate_response(
        "Welcome AltoTech's lovely investors to the 4th AGM 2025. Give a very brief, engaging introduction to this podcast about AltoTech and smart building solutions. You are happy to be the host today."
    )
    console.print_host(opening)
    
    # Topics to cover
    topics = list(TopicArea)
    current_topic_idx = 0
    
    # Initialize podcast state
    state = PodcastState(current_topic=topics[current_topic_idx])
    
    # Main conversation loop
    while current_topic_idx < len(topics):
        topic = topics[current_topic_idx]
        console.print_topic(topic.display_name)
        
        # Host question - with context if we have previous exchanges
        topic_exchanges = state.get_current_topic_exchanges()
        context = "\n".join(topic_exchanges) if topic_exchanges else ""
        prompt = (
            f"Ask a follow-up question about {topic.display_name}, building upon this context:\n{context}"
            if context else
            f"Ask about {topic.display_name}"
        )
        
        # Get previous topic if we just transitioned
        previous_topic = topics[current_topic_idx - 1].value if current_topic_idx > 0 else ""
        
        host_response = await host.generate_response(
            prompt,
            topic=topic.value,
            previous_topic=previous_topic
        )
        console.print_host(host_response)
        state.add_dialogue({"role": "host", "content": host_response, "dialogue_type": "question"})
        
        # Guest response
        guest_response = await guest.generate_response(
            host_response,
            topic=topic.value
        )
        console.print_guest(guest_response)
        state.add_dialogue({"role": "guest", "content": guest_response, "dialogue_type": "response"})
        
        # Check for audience questions
        if question := prompts.get_audience_question():
            console.print_audience(question)
            state.add_audience_question(question)
            
            # Host acknowledges previous response and asks audience question
            host_followup = await host.generate_response(
                f"Address this audience question: {question}",
                previous_response=guest_response,
                audience_question=question,
                topic=topic.value
            )
            console.print_host(host_followup)
            state.add_dialogue({"role": "host", "content": host_followup, "dialogue_type": "question"})
            
            # Guest responds to audience
            guest_followup = await guest.generate_response(
                host_followup,
                topic=topic.value
            )
            console.print_guest(guest_followup)
            state.add_dialogue({"role": "guest", "content": guest_followup, "dialogue_type": "response"})
        
        # Get recent conversation history
        recent_exchanges = state.get_current_topic_exchanges()
        
        # Check if we should end the podcast
        if await prompts.should_end_podcast(topic, recent_exchanges):
            break
            
        # Check if we should move to the next topic
        if await prompts.should_continue(topic, recent_exchanges):
            current_topic_idx += 1
            if current_topic_idx < len(topics):
                state.current_topic = topics[current_topic_idx]
    
    # Closing remarks
    closing = await host.generate_response(
        "Give a brief, positive closing remark about AltoTech's potential impact on energy sustainability."
    )
    console.print_host(closing)
    
    # End podcast
    console.print_footer()

if __name__ == "__main__":
    asyncio.run(run_podcast())