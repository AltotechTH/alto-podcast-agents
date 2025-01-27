from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Tuple
import json
import asyncio
import uvicorn
import time
from random import choice

# Import podcast components
from agents.host import ElonMuskHost
from agents.guest import AltoTechCEO
from models.state import PodcastState
from models.enums import TopicArea
from ui.console import PodcastConsole
from ui.prompts import PodcastPrompts

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock conversation data
LEFT_RESPONSES = [
    "Hello! I'm the left agent. How can I help you today?",
    "That's interesting! Tell me more about that.",
    "I understand your perspective. Let me share my thoughts.",
    "From my analysis, we should consider multiple approaches.",
    "I agree with that assessment. Shall we explore further?"
]

RIGHT_RESPONSES = [
    "Greetings! Right agent here. I have a different view on this.",
    "Actually, let me add to what the left agent mentioned.",
    "I see it from another angle. Here's my perspective.",
    "Interesting point! I'd like to build on that idea.",
    "Let me offer an alternative approach to consider."
]

# Store active connections and speaking states
class ConnectionManager:
    def __init__(self):
        # Dictionary to store connections for different sessions
        self.sessions: Dict[str, List[WebSocket]] = {
            "left": [],
            "right": [],
            "audience": []  # Add audience session
        }
        # Track speaking states
        self.speaking_states = {
            "leftIsSpeaking": False,
            "rightIsSpeaking": False,
            "audienceIsSpeaking": False  # Add audience speaking state
        }
        # Podcast components
        self.host = None
        self.guest = None
        self.state = None
        self.is_podcast_running = False
        # Priority queue for messages with timestamps
        self.message_queue = asyncio.PriorityQueue()
        # Background task for processing queue
        self.queue_task = None
        # Event for queue empty notification
        self.queue_empty = asyncio.Event()
        self.queue_empty.set()  # Initially set to True as queue is empty

    async def connect(self, websocket: WebSocket, session: str):
        await websocket.accept()
        self.sessions[session].append(websocket)
        print(f"New connection to {session} session")
        
        # Start queue processor if not running
        if self.queue_task is None or self.queue_task.done():
            self.queue_task = asyncio.create_task(self.process_queue())

    def disconnect(self, websocket: WebSocket, session: str):
        if websocket in self.sessions[session]:
            self.sessions[session].remove(websocket)
            print(f"Disconnected from {session} session")
            
            # Cancel queue processor if no connections in any session
            if not any(self.sessions.values()) and self.queue_task:
                self.queue_task.cancel()
                self.queue_task = None

    async def wait_for_queue_empty(self):
        """Wait for the queue to be empty"""
        await self.queue_empty.wait()

    async def process_queue(self):
        """Background task to process message queue"""
        while True:
            try:
                # Wait for a message in the queue
                timestamp, (message, session) = await self.message_queue.get()
                self.queue_empty.clear()  # Queue has items
                
                # Skip if any agent is speaking
                if any(self.speaking_states.values()):
                    # Put the message back at the front of the queue with original timestamp
                    await self.message_queue.put((timestamp, (message, session)))
                    self.message_queue.task_done()
                    await asyncio.sleep(0.1)  # Small delay before next attempt
                    continue
                
                # Send message to all connections in the session
                dead_connections = []
                print(f"\nProcessing queued message for {session} session:")
                print(f"Message: {message}")
                print(f"Active connections: {len(self.sessions[session])}")

                # Set speaking state before broadcasting
                self.speaking_states[f"{session}IsSpeaking"] = True
                
                if not self.sessions[session]:
                    print(f"No active connections for {session} session")
                    self.message_queue.task_done()
                    self.speaking_states[f"{session}IsSpeaking"] = False
                    continue
                
                for connection in self.sessions[session]:
                    try:
                        await connection.send_json({
                            "text": message,
                            "session": session
                        })
                    except:
                        dead_connections.append(connection)
                        print(f"Failed to send to a connection in {session} session")

                # Clean up dead connections
                for dead in dead_connections:
                    if dead in self.sessions[session]:
                        self.sessions[session].remove(dead)
                        print(f"Removed dead connection from {session} session")
                
                print(f"Message processed. Remaining connections: {len(self.sessions[session])}\n")
                # Only mark as done after successful processing
                self.message_queue.task_done()
                
                # Check if queue is empty and set event if it is
                if self.message_queue.empty():
                    self.queue_empty.set()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing queue: {str(e)}")
                # Reset speaking state on error
                if 'session' in locals():
                    self.speaking_states[f"{session}IsSpeaking"] = False
                await asyncio.sleep(0.1)  # Small delay before retrying

    async def broadcast(self, message: str, session: str):
        """Add message to queue for broadcasting"""
        # Use timestamp as priority (lower timestamp = higher priority)
        timestamp = int(time.time() * 1000)  # millisecond timestamp
        self.queue_empty.clear()  # Queue will have items
        
        # Remove "Host:" prefix if present
        if message.startswith("Host:"):
            message = message[5:].strip()
            
        await self.message_queue.put((timestamp, (message, session)))
        print(f"Added message to queue. Queue size: {self.message_queue.qsize()}")

    def update_speaking_state(self, state_update: dict):
        # Update speaking states
        if "leftIsSpeaking" in state_update:
            self.speaking_states["leftIsSpeaking"] = state_update["leftIsSpeaking"]
        if "rightIsSpeaking" in state_update:
            self.speaking_states["rightIsSpeaking"] = state_update["rightIsSpeaking"]
        
        # Print current speaking states
        print("\nCurrent speaking states:")
        print(f"Left agent speaking: {self.speaking_states['leftIsSpeaking']}")
        print(f"Right agent speaking: {self.speaking_states['rightIsSpeaking']}\n")

    async def run_podcast(self):
        """Run the podcast conversation"""
        print("Starting podcast conversation")
        prompts = PodcastPrompts()
        prompts.clear_submissions()
        if self.is_podcast_running:
            return
            
        self.is_podcast_running = True
        self.host = ElonMuskHost()
        self.guest = AltoTechCEO()
        self.state = PodcastState(current_topic=TopicArea.COMPANY_GROWTH)
        
        # Opening
        opening = await self.host.generate_response(
            "Welcome AltoTech's lovely investors to the 4th AGM 2025. Give a very brief (1-3 sentences), engaging introduction to this talk about AltoTech and smart building solutions. You are happy to be the host today."
        )
        await self.broadcast(opening, "left")
        await self.wait_for_queue_empty()
        
        # Topics to cover
        topics = list(TopicArea)
        current_topic_idx = 0
        
        # Main conversation loop
        while current_topic_idx < len(topics) and self.is_podcast_running:
            topic = topics[current_topic_idx]
            
            # Host question
            topic_exchanges = self.state.get_current_topic_exchanges()
            context = "\n".join(topic_exchanges) if topic_exchanges else ""
            prompt = (
                f"Ask a follow-up question about {topic.display_name}, building upon this context:\n{context}"
                if context else
                f"Ask about {topic.display_name}"
            )
            
            previous_topic = topics[current_topic_idx - 1].value if current_topic_idx > 0 else ""
            
            host_response = await self.host.generate_response(
                prompt,
                topic=topic.value,
                previous_topic=previous_topic
            )
            await self.broadcast(host_response, "left")
            self.state.add_dialogue({"role": "host", "content": host_response, "dialogue_type": "question"})
            await self.wait_for_queue_empty()
            
            # Guest response
            guest_response = await self.guest.generate_response(
                host_response,
                topic=topic.value
            )
            await self.broadcast(guest_response, "right")
            self.state.add_dialogue({"role": "guest", "content": guest_response, "dialogue_type": "response"})
            await self.wait_for_queue_empty()
            
            # Check for audience questions
            while True:
                
                question = prompts.get_audience_question()
                if question is None:
                    break
                
                self.state.add_audience_question(question)
                
                # Host acknowledges previous response and asks audience question
                host_followup = await self.host.generate_response(
                    f"Address this audience question: {question}",
                    previous_response=guest_response,
                    audience_question=question,
                    topic=topic.value
                )
                await self.broadcast(host_followup, "left")
                self.state.add_dialogue({"role": "host", "content": host_followup, "dialogue_type": "question"})
                await self.wait_for_queue_empty()
                
                # Guest responds to audience
                guest_followup = await self.guest.generate_response(
                    host_followup,
                    topic=topic.value
                )
                await self.broadcast(guest_followup, "right")
                self.state.add_dialogue({"role": "guest", "content": guest_followup, "dialogue_type": "response"})
                await self.wait_for_queue_empty()
            
            # Get recent conversation history
        #     recent_exchanges = self.state.get_current_topic_exchanges()
            
        #     # Check if we should end the podcast
        #     if await prompts.should_end_podcast(topic, recent_exchanges):
        #         break
                
        #     # Check if we should move to the next topic
        #     if await prompts.should_continue(topic, recent_exchanges):
        #         current_topic_idx += 1
        #         if current_topic_idx < len(topics):
        #             self.state.current_topic = topics[current_topic_idx]
        
        # # Closing remarks
        # closing = await self.host.generate_response(
        #     "Give a brief, positive closing remark about AltoTech's potential impact on energy sustainability."
        # )
        # await self.broadcast(closing, "left")
        # await self.wait_for_queue_empty()
            
        self.is_podcast_running = False

manager = ConnectionManager()

@app.websocket("/ws/{session}")
async def websocket_endpoint(websocket: WebSocket, session: str):
    if session not in ["left", "right", "audience"]:  # Add audience to valid sessions
        await websocket.close(code=4000)
        return

    await manager.connect(websocket, session)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from {session}: {data[:100]}...")
            try:
                message = json.loads(data)
                if message.get("type") == "speaking_state":
                    # Handle speaking state updates
                    manager.update_speaking_state(message)
                else:
                    # Handle regular messages
                    await manager.broadcast(data, session)
            except json.JSONDecodeError:
                # Handle plain text messages
                await manager.broadcast(data, session)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session)

@app.post("/send_message/{session}")
async def send_message(message: str, session: str):
    if session not in ["left", "right", "audience"]:  # Add audience to valid sessions
        return {"error": "Invalid session"}
    await manager.broadcast(message, session)
    return {"status": f"Message sent to {session} session"}

@app.post("/test/start_conversation")
async def start_test_conversation():
    """Start a mock conversation between the two agents"""
    async def simulate_conversation():
        for _ in range(5):  # Will send 5 messages back and forth
            # Left agent speaks
            await asyncio.sleep(2)
            await manager.broadcast(choice(LEFT_RESPONSES), "left")
            
            # Right agent responds
            await asyncio.sleep(2)
            await manager.broadcast(choice(RIGHT_RESPONSES), "right")
    
    # Start the conversation in the background
    asyncio.create_task(simulate_conversation())
    return {"status": "Started test conversation"}

@app.post("/podcast/start")
async def start_podcast():
    """Start the AI podcast conversation"""
    if not manager.is_podcast_running:
        # Start the podcast in the background
        asyncio.create_task(manager.run_podcast())
        return {"status": "Started podcast conversation"}
    return {"status": "Podcast is already running"}

@app.post("/podcast/stop")
async def stop_podcast():
    """Stop the running podcast"""
    if manager.is_podcast_running:
        manager.is_podcast_running = False
        return {"status": "Stopping podcast"}
    return {"status": "No podcast running"}

@app.get("/ping")
async def ping():
    """Ping the server"""
    return {"status": "pong"}

if __name__ == "__main__":
    print("Starting WebSocket server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)