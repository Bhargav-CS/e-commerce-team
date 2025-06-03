from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # type: ignore
import os

MODEL = os.getenv("MODEL", "azure/gpt-4o")

def check_inventory(product_id: str) -> dict:
    stock = {"shirt-blue": 12, "pants-black": 0}
    if product_id in stock:
        return {"status": "success", "stock": stock[product_id]}
    return {"status": "error", "error_message": "Product not found."}

inventory_agent = Agent(
    name="inventory_agent",
    model=LiteLlm(model=MODEL),
    description="Checks product stock levels.",
    instruction="Use `check_inventory` to answer product availability questions.",
    tools=[check_inventory],
    sub_agents=[]
)
