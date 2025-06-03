from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def track_shipment(order_id: str) -> dict:
    return {"status": "success", "message": f"Order {order_id} is in transit and will arrive tomorrow."}

shipping_agent = Agent(
    name="shipping_agent",
    model=LiteLlm(model=MODEL),
    description="Tracks orders and handles delivery inquiries.",
    instruction="Use `track_shipment` to check the delivery status of an order.",
    tools=[track_shipment],
    sub_agents=[]
)
