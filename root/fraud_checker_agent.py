from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def check_fraud(user_id: str) -> dict:
    if user_id == "suspicious_user":
        return {"status": "error", "error_message": "User flagged for fraud."}
    return {"status": "success", "message": "User clear."}

fraud_checker_agent = Agent(
    name="fraud_checker_agent",
    model=LiteLlm(model=MODEL),
    description="Checks if the user is suspicious.",
    instruction="Use `check_fraud` to detect fraud risk for a user.",
    tools=[check_fraud],
    sub_agents=[]
)
