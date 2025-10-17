"""Mock implementation for the `places.search` tool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Place:
    place_id: str
    name: str
    cuisines: List[str]
    tags: List[str]
    price_level: int
    distance_km: float


class PlacesSearchTool:
    """In-memory search over a seed catalogue.

    Replace the `_catalogue` loader with a connector to Google Places, Yelp, or
    another local search provider. The `search` method mirrors the JSON schema
    included in the project blueprint.
    """

    def __init__(self, catalogue: Optional[Iterable[Dict[str, Any]]] = None) -> None:
        self._catalogue = [
            Place(
                place_id="demo-ramen",
                name="Ramen Zen",
                cuisines=["japanese"],
                tags=["vegan", "spicy"],
                price_level=2,
                distance_km=1.2,
            ),
            Place(
                place_id="demo-pizza",
                name="Slice Society",
                cuisines=["italian"],
                tags=["vegetarian", "gluten-free"],
                price_level=1,
                distance_km=0.8,
            ),
        ]
        if catalogue:
            self._catalogue.extend(Place(**item) for item in catalogue)

    def search(
        self,
        near: str,
        cuisines: Optional[List[str]] = None,
        dietary: Optional[List[str]] = None,
        max_price: Optional[float] = None,
        distance_km: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        del near  # geo filtering mocked out
        cuisines = [c.lower() for c in cuisines or []]
        dietary = {d.lower() for d in dietary or []}

        results: List[Dict[str, Any]] = []
        for place in self._catalogue:
            if cuisines and not any(c in place.cuisines for c in cuisines):
                continue
            if distance_km is not None and place.distance_km > distance_km:
                continue
            if max_price is not None and place.price_level > max_price:
                continue
            if dietary and not dietary.issubset({tag.lower() for tag in place.tags}):
                continue
            results.append(
                {
                    "place_id": place.place_id,
                    "name": place.name,
                    "cuisines": place.cuisines,
                    "tags": place.tags,
                    "price_level": place.price_level,
                    "distance_km": place.distance_km,
                }
            )
        return results
