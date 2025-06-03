from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def get_return_policy(product_id: str) -> dict:
    return {"status": "success", "policy": f"{product_id} can be returned within 30 days."}

policy_checker_agent = Agent(
    name="policy_checker_agent",
    model=LiteLlm(model=MODEL),
    description="Reads return policy for a given product.",
    instruction="Use `get_return_policy` to determine if a product is eligible for return.",
    tools=[get_return_policy],
    sub_agents=[]
)
