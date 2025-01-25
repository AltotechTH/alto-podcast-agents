# altotech_podcast/context/company.py
from typing import Any
from pydantic import BaseModel, Field

class CompanyMetrics(BaseModel):
    """Key business metrics for the company."""
    revenue: str = "$0.7M"
    growth_rate: str = "388% YoY"
    funding_raised: str = "$2.4M"
    managed_area: str = "3M+ sqm"
    target_raise: str = "$8M Series A"
    energy_savings: str = "40%"
    payback_period: str = "<3 years"

class CustomerSuccess(BaseModel):
    """Customer success stories and metrics."""
    name: str
    location: str
    results: dict[str, Any]
    testimonial: str | None = None

class CompanyContext(BaseModel):
    """Complete company context and knowledge base."""
    name: str = "AltoTech Global"
    description: str = "Energy management platform optimizing HVAC systems"
    metrics: CompanyMetrics = Field(default_factory=CompanyMetrics)
    
    key_milestones: list[str] = [
        "First foreign customer acquisition in Singapore",
        "Top 10 startups award at APAC Climate Tech Summit",
        "Premium customer testimonials from 5-star hotels",
        "Strategic MOUs with major property developers",
        "Patent pending for AI-driven HVAC optimization",
        "Launch of real-time energy monitoring dashboard"
    ]
    
    success_stories: list[CustomerSuccess] = [
        CustomerSuccess(
            name="Luxury Hotel Group",
            location="Bangkok",
            results={"energy_savings": "45%", "annual_cost_reduction": "$120K"},
            testimonial="AltoTech's system paid for itself in under 2 years"
        ),
        CustomerSuccess(
            name="Premium Mall",
            location="Singapore",
            results={"energy_savings": "38%", "co2_reduction": "500 tons/year"},
            testimonial="Helped us achieve our sustainability goals ahead of schedule"
        )
    ]
    
    challenges_overcome: list[str] = [
        "Building trust with conservative property managers",
        "Adapting AI models to different building types",
        "Scaling installation and support across countries",
        "Managing varying regulatory requirements"
    ]
    
    future_goals: list[str] = [
        "Expand to 5 new markets in Asia-Pacific",
        "Launch new product for smaller commercial buildings",
        "Develop predictive maintenance capabilities",
        "Achieve carbon credit certification"
    ]
    
    def format_for_prompt(self) -> str:
        """Format company context for use in agent prompts."""
        return f"""Company: {self.name}
Description: {self.description}

Key Metrics:
- Revenue: {self.metrics.revenue}
- Growth: {self.metrics.growth_rate}
- Managed Area: {self.metrics.managed_area}
- Typical Energy Savings: {self.metrics.energy_savings}
- Current Funding: {self.metrics.funding_raised}
- Target Raise: {self.metrics.target_raise}

Recent Milestones:
{chr(10).join(f"- {m}" for m in self.key_milestones)}

Customer Success:
{chr(10).join(
    f"- {cs.name} ({cs.location}): {cs.results['energy_savings']} savings"
    for cs in self.success_stories
)}"""