from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def place_order(product_id: str, quantity: int) -> dict:
    if product_id == "shirt-blue" and quantity <= 12:
        return {
            "status": "success",
            "order_id": "ORD123456",
            "message": f"Order placed for {quantity}x {product_id}."
        }
    return {"status": "error", "error_message": "Insufficient stock."}

order_agent = Agent(
    name="order_agent",
    model=LiteLlm(model=MODEL),
    description="Places and tracks orders.",
    instruction="Use `place_order` to place a new order.",
    tools=[place_order],
    sub_agents=[]
)
