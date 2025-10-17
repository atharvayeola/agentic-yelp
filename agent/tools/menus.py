"""Menu lookup tool scaffolding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MenuItem:
    place_id: str
    item_id: str
    name: str
    price: float
    tags: List[str]
    cuisine: List[str]


class MenuLookupTool:
    """Fetch menu items from an in-memory store or DynamoDB."""

    def __init__(self, items: Optional[List[Dict[str, Any]]] = None) -> None:
        self._items = [
            MenuItem(
                place_id="demo-ramen",
                item_id="miso-vegan",
                name="Vegan Miso Ramen",
                price=16.5,
                tags=["vegan", "spicy"],
                cuisine=["japanese"],
            ),
            MenuItem(
                place_id="demo-pizza",
                item_id="gf-margherita",
                name="Gluten-Free Margherita",
                price=14.0,
                tags=["vegetarian", "gluten-free"],
                cuisine=["italian"],
            ),
        ]
        if items:
            self._items.extend(MenuItem(**item) for item in items)

    def lookup(self, place_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "place_id": item.place_id,
                "item_id": item.item_id,
                "name": item.name,
                "price": item.price,
                "tags": item.tags,
                "cuisine": item.cuisine,
            }
            for item in self._items
            if item.place_id == place_id
        ]
