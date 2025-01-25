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
    console.print_header()
    
    # Opening
    opening = await host.generate_response(
        "Give a brief, engaging introduction to this podcast about AltoTech and energy innovation."
    )
    console.print_host(opening)
    
    # Topics to cover
    topics = list(TopicArea)
    current_topic_idx = 0
    
    # Track conversation history per topic
    topic_exchanges: Dict[TopicArea, List[str]] = {topic: [] for topic in topics}
    
    # Main conversation loop
    while current_topic_idx < len(topics):
        topic = topics[current_topic_idx]
        console.print_topic(topic.display_name)
        
        # Host question - with context if we have previous exchanges
        context = "\n".join(topic_exchanges[topic]) if topic_exchanges[topic] else ""
        prompt = (
            f"Ask a follow-up question about {topic.display_name}, building upon this context:\n{context}"
            if context else
            f"Ask about {topic.display_name}"
        )
        
        host_response = await host.generate_response(
            prompt,
            topic=topic.value
        )
        console.print_host(host_response)
        topic_exchanges[topic].append(f"Host: {host_response}")
        
        # Guest response
        guest_response = await guest.generate_response(
            host_response,
            topic=topic.value
        )
        console.print_guest(guest_response)
        topic_exchanges[topic].append(f"Guest: {guest_response}")
        
        # Check for audience questions
        if question := prompts.get_audience_question():
            console.print_audience(question)
            
            # Host acknowledges previous response and asks audience question
            host_followup = await host.generate_response(
                f"Address this audience question: {question}",
                previous_response=guest_response,
                audience_question=question
            )
            console.print_host(host_followup)
            topic_exchanges[topic].append(f"Audience: {question}")
            topic_exchanges[topic].append(f"Host: {host_followup}")
            
            # Guest responds to audience
            guest_followup = await guest.generate_response(
                host_followup,
                topic=topic.value
            )
            console.print_guest(guest_followup)
            topic_exchanges[topic].append(f"Guest: {guest_followup}")
        
        # Continue to next topic?
        if prompts.should_continue():
            current_topic_idx += 1
        else:
            # Ask if they want to end the podcast
            if prompts.should_end_podcast():
                break
            # Otherwise stay on current topic for more discussion
    
    # Closing remarks
    closing = await host.generate_response(
        "Give a brief, positive closing remark about AltoTech's potential impact on energy sustainability."
    )
    console.print_host(closing)
    
    # End podcast
    console.print_footer()

if __name__ == "__main__":
    asyncio.run(run_podcast())