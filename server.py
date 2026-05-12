# server.py
"""
Simple MCP server in Python with 2 tools using Fake Store API.

Tools:
1. get_products(limit=10)
2. search_products(query)

Works with:
- ChatGPT Connectors (MCP)
- Claude Desktop MCP connector

Requirements:
    pip install fastmcp httpx

Run:
    python server.py

Fake Store API:
    https://fakestoreapi.com/
"""

from typing import List, Dict, Any
import httpx
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("FakeStore MCP Server")

BASE_URL = "https://fakestoreapi.com/products"


# -------------------------------------------------------------------
# Tool 1: Get Products
# -------------------------------------------------------------------
@mcp.tool()
async def get_products(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get products from Fake Store API.

    Args:
        limit: Number of products to return

    Returns:
        List of products
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)

        response.raise_for_status()

        products = response.json()

        return products[:limit]


# -------------------------------------------------------------------
# Tool 2: Search Products
# -------------------------------------------------------------------
@mcp.tool()
async def search_products(query: str) -> List[Dict[str, Any]]:
    """
    Search products by title/category/description.

    Args:
        query: Search text

    Returns:
        Matching products
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)

        response.raise_for_status()

        products = response.json()

    query = query.lower()

    filtered = []

    for product in products:
        searchable = " ".join([
            str(product.get("title", "")),
            str(product.get("description", "")),
            str(product.get("category", "")),
        ]).lower()

        if query in searchable:
            filtered.append(product)

    return filtered


# -------------------------------------------------------------------
# Start MCP server
# -------------------------------------------------------------------
if __name__ == "__main__":
    # stdio transport works with Claude Desktop and ChatGPT connectors
    mcp.run()