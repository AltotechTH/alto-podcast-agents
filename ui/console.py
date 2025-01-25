# altotech_podcast/ui/console.py
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class SpeakerStyle(str, Enum):
    """Styles for different speakers in the podcast."""
    HOST = "bold red"
    GUEST = "bold blue"
    AUDIENCE = "bold green"
    SYSTEM = "bold yellow"
    INFO = "dim"

class PodcastConsole:
    """Handles formatted console output for the podcast."""
    
    def __init__(self):
        self.console = Console()
    
    def print_header(self) -> None:
        """Print the podcast header."""
        self.console.print("\n🎙️ [bold yellow]Tech Frontiers Podcast with Elon Musk[/bold yellow] 🎙️", justify="center")
        self.console.print("[bold yellow]The Future of Energy Management in the AI Era[/bold yellow]\n", justify="center")
    
    def print_footer(self) -> None:
        """Print the podcast footer."""
        self.console.print("\n[bold yellow]End of Podcast[/bold yellow] 🎬\n", justify="center")
    
    def print_host(self, message: str) -> None:
        """Print host's dialogue."""
        self.print_dialogue("🎤 Elon:", message, SpeakerStyle.HOST)
    
    def print_guest(self, message: str) -> None:
        """Print guest's dialogue."""
        self.print_dialogue("💼 AltoTech CEO:", message, SpeakerStyle.GUEST)
    
    def print_audience(self, message: str) -> None:
        """Print audience question."""
        self.print_dialogue("👥 Audience:", message, SpeakerStyle.AUDIENCE)
    
    def print_info(self, message: str) -> None:
        """Print system/info message."""
        self.console.print(f"[{SpeakerStyle.INFO}]{message}[/{SpeakerStyle.INFO}]")
    
    def print_topic(self, topic: str) -> None:
        """Print new topic header."""
        self.console.print(f"\n📌 [bold yellow]New Topic: {topic}[/bold yellow]\n")
    
    def print_dialogue(self, speaker: str, message: str, style: SpeakerStyle) -> None:
        """Print formatted dialogue."""
        text = Text()
        text.append(f"\n{speaker} ", style=style)
        text.append(message)
        self.console.print(text)
    
    def create_panel(self, content: Any, title: str) -> Panel:
        """Create a bordered panel with content."""
        return Panel(str(content), title=title, border_style="bold yellow")

    def print_metrics(self, metrics: dict[str, Any]) -> None:
        """Print metrics in a formatted panel."""
        content = "\n".join(f"{k}: {v}" for k, v in metrics.items())
        self.console.print(self.create_panel(content, "📊 Metrics"))