# tools/math_tools.py
from langchain_core.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b
