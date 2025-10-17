"""Booking helper tool stubs."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class BookingTools:
    """Generate booking deeplinks and calendar entries."""

    def make_deeplink(self, place_id: str, party_size: int, datetime_iso: str) -> Dict[str, str]:
        """Return a deterministic booking deeplink."""

        return {
            "url": (
                "https://book.example.com/"
                f"?place={place_id}&party={party_size}&dt={datetime_iso}"
            )
        }

    def create_calendar_event(self, title: str, start_iso: str, end_iso: str, location: str) -> Dict[str, str]:
        """Mock calendar event creation."""

        _validate_iso(start_iso)
        _validate_iso(end_iso)
        return {
            "title": title,
            "start_iso": start_iso,
            "end_iso": end_iso,
            "location": location,
            "status": "tentative",
        }


def _validate_iso(value: str) -> None:
    datetime.fromisoformat(value.replace("Z", "+00:00"))
