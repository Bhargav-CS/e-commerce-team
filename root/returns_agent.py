from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os
from .policy_checker_agent import policy_checker_agent

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def process_return(order_id: str) -> dict:
    return {"status": "success", "message": f"Return initiated for {order_id}."}

returns_agent = Agent(
    name="returns_agent",
    model=LiteLlm(model=MODEL),
    description="Handles returns and eligibility checks.",
    instruction="Use `process_return` to start return. Delegate policy check to policy_checker_agent.",
    tools=[process_return],
    sub_agents=[policy_checker_agent]
)
