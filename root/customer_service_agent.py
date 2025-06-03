from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os
from .inventory_agent import inventory_agent
from .order_agent import order_agent
from .payments_agent import payments_agent
from .shipping_agent import shipping_agent
from .returns_agent import returns_agent

MODEL = os.getenv("MODEL", "azure/gpt-4o")

customer_service_agent = Agent(
    name="customer_service_agent",
    model=LiteLlm(model=MODEL),
    description="E-commerce assistant that handles customer queries and delegates tasks.",
    instruction=(
        "You handle customer requests.\n"
        "- Delegate to inventory_agent for stock questions.\n"
        "- Delegate to order_agent for placing orders.\n"
        "- Delegate to payments_agent for payment/refund.\n"
        "- Delegate to shipping_agent for tracking.\n"
        "- Delegate to returns_agent for return inquiries.\n"
    ),
    tools=[],
    sub_agents=[
        inventory_agent,
        order_agent,
        payments_agent,
        shipping_agent,
        returns_agent,
    ]
)
