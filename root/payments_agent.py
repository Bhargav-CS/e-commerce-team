from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
from google.adk.tools.tool_context import ToolContext
import os
from .fraud_checker_agent import fraud_checker_agent

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def charge_card(tool_context:ToolContext) -> dict:
    return {"status": "success", "transaction_id": "TXN789", "message": "Payment processed."}

def refund(transaction_id: str) -> dict:
    return {"status": "success", "message": f"Refund issued for {transaction_id}."}

payments_agent = Agent(
    name="payments_agent",
    model=LiteLlm(model=MODEL),
    description="Processes payments and refunds.",
    instruction=(
        "Use `charge_card` to process payments and `refund` to process refunds. "
        "Call fraud_checker_agent if fraud check is needed."
    ),
    tools=[charge_card, refund],
    sub_agents=[fraud_checker_agent]
)
