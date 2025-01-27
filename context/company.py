# altotech_podcast/context/company.py
from typing import Any
from pydantic import BaseModel, Field

class CompanyMetrics(BaseModel):
    """Key business metrics for AltoTech Global."""
    revenue: str = "$0.7M (2024)"
    growth_rate: str = "388% YoY"
    funding_raised: str = "$2.4M (including $50K Founders, $250K Seed, $2.1M Pre-A)"
    managed_area: str = "3M+ sqm"
    target_raise: str = "$8M Series A"
    energy_savings: str = "Up to 40%"
    payback_period: str = "<3 years"
    properties_commissioned: str = "68+"
    carbon_reduction: str = "2.8M KgCO2eq"
    energy_managed: str = "129 GWh"
    customer_retention: str = "95%"
    customer_conversion: str = "25%"

class CustomerSuccess(BaseModel):
    """Customer success stories and metrics."""
    name: str
    location: str
    results: dict[str, Any]
    testimonial: str | None = None

class CompanyContext(BaseModel):
    """AltoTech Global company context from official documents."""
    name: str = "AltoTech Global"
    description: str = "AI and data-driven solutions provider managing air-side and water-side systems to reduce energy consumption, enhance operational efficiency, and drive sustainability across diverse industries."
    metrics: CompanyMetrics = Field(default_factory=CompanyMetrics)
    
    key_milestones: list[str] = [
        "MOU with PEA in Thailand for national energy initiatives",
        "Partnership with C&W Services in Singapore",
        "Partnership with Telemax and Hong Kong Science Park",
        "Top 10 E27 Startups in Singapore",
        "Only AI and software focused member of Tridium in Thailand, 1 of only 3 next to Honeywell and Johnson Controls in Thailand"
    ]
    
    success_stories: list[CustomerSuccess] = [
        CustomerSuccess(
        name="JW Marriott & St. Regis",
        location="Thailand",
        results={
            "energy_savings": "Up to 40%",
            "operational_efficiency": "300%",
            "payback_period": "<3 years"
        },
        testimonial="The ROI is reasonably fast; it is obviously a big win while also providing opportunities such as improving guest experience"
    ),
    
    # Commercial Buildings
    CustomerSuccess(
        name="MBK Center",
        location="Thailand",
        results={
            "building_performance": "Improved",
            "energy_savings": "Significant",
            "indoor_air_quality": "Enhanced"
        },
        testimonial="Energy management solutions have significantly reduced operational costs, improved building performance and indoor air quality"
    ),
    
    CustomerSuccess(
        name="Central Plaza Rama 9",
        location="Thailand",
        results={
            "building_performance": "Improved",
            "operational_costs": "Reduced",
            "indoor_air_quality": "Enhanced"
        }
    ),
    
    # International
    CustomerSuccess(
        name="Great Eastern",
        location="Singapore",
        results={
            "automation": "Complete",
            "manpower_efficiency": "Significant",
            "task_management": "AI-integrated"
        },
        testimonial="Previously, we relied on manual data recording and reporting. With Alto, everything is automated, reducing manpower significantly. The AI integration helps manage tasks, prioritize, and organize schedules effectively"
    )
    
    
    ]
    
    challenges_overcome: list[str] = [
        "Scaling across multiple property types (hotels, offices, hospitals)",
        "Integration with diverse building management systems",
        "Market education on AI-driven energy management",
        "Regional expansion and localization"
    ]
    
    future_goals: list[str] = [
        "Expand further in SEA markets",
        "Develop cutting-edge AI capabilities",
        "Launch new platform for demand response and energy trading",
        "Advance towards smart city management initiatives"
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
- Carbon Reduction: {self.metrics.carbon_reduction}
- Energy Managed: {self.metrics.energy_managed}
- Properties Commissioned: {self.metrics.properties_commissioned}
- Payback Period: {self.metrics.payback_period}
- Customer Retention: {self.metrics.customer_retention}
- Customer Conversion: {self.metrics.customer_conversion}

Recent Milestones:
{chr(10).join(f"- {m}" for m in self.key_milestones)}

Customer Success:
{chr(10).join(
    f"- {cs.name} ({cs.location}): {cs.results['energy_savings']} savings"
    for cs in self.success_stories
)}"""