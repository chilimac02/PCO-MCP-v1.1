"""
Planning Center API Client
Handles authentication and data retrieval from Planning Center People API.
"""

import os
import requests
from base64 import b64encode
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class PCOClient:
    """Client for interacting with Planning Center People API."""

    BASE_URL = "https://api.planningcenteronline.com/people/v2"

    def __init__(self, app_id: str = None, secret: str = None):
        self.app_id = app_id or os.getenv("PCO_APP_ID")
        self.secret = secret or os.getenv("PCO_SECRET")

        print(f"[DEBUG] PCO_APP_ID: {self.app_id}")
        print(f"[DEBUG] PCO_SECRET: {self.secret[:20] if self.secret else 'None'}...")

        if not self.app_id or not self.secret:
            raise ValueError(
                "PCO_APP_ID and PCO_SECRET must be set in environment or .env file"
            )

        self._session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self):
        """Set Basic Auth header using app_id and secret."""
        credentials = b64encode(f"{self.app_id}:{self.secret}".encode()).decode()
        print(f"[DEBUG] Auth header: Basic {credentials[:30]}...")
        self._session.headers.update({
            "Authorization": f"Basic {credentials}",
            "X-API-Version": "2024-01-17",  # PCO API version header
        })

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the PCO API."""
        url = f"{self.BASE_URL}/{endpoint}"
        print(f"[DEBUG] GET {url}")
        print(f"[DEBUG] Params: {params}")
        print(f"[DEBUG] Headers: {dict(self._session.headers)}")
        
        response = self._session.get(url, params=params)
        print(f"[DEBUG] Response: {response.status_code} {response.text[:200]}")
        response.raise_for_status()
        return response.json()

    # --- People Endpoints ---

    def get_people(self, per_page: int = 100, offset: int = 0) -> List[Dict]:
        """Get all people."""
        params = {"per_page": per_page, "offset": offset}
        data = self._get("people", params)
        return data.get("data", [])

    def search_people(self, query: str) -> List[Dict]:
        """Search people by name or email."""
        params = {"search": query}
        data = self._get("people", params)
        return data.get("data", [])

    def get_person(self, person_id: str) -> Dict:
        """Get a specific person by ID."""
        return self._get(f"people/{person_id}")

    def get_person_field_values(self, person_id: str) -> List[Dict]:
        """Get custom field values for a person."""
        data = self._get(f"people/{person_id}/field_values")
        return data.get("data", [])

    # --- Groups Endpoints ---

    def get_groups(self, per_page: int = 100) -> List[Dict]:
        """Get all groups."""
        data = self._get("groups", {"per_page": per_page})
        return data.get("data", [])

    def get_group(self, group_id: str) -> Dict:
        """Get a specific group."""
        return self._get(f"groups/{group_id}")

    def get_group_members(self, group_id: str, per_page: int = 100) -> List[Dict]:
        """Get members of a group."""
        data = self._get(f"groups/{group_id}/memberships", {"per_page": per_page})
        return data.get("data", [])

    def get_group_types(self) -> List[Dict]:
        """Get all group types."""
        data = self._get("group_types")
        return data.get("data", [])

    # --- Tags ---

    def get_tags(self) -> List[Dict]:
        """Get all tags."""
        data = self._get("tags")
        return data.get("data", [])

    def get_people_with_tag(self, tag_id: str) -> List[Dict]:
        """Get people with a specific tag."""
        data = self._get(f"tags/{tag_id}/people")
        return data.get("data", [])

    # --- Households ---

    def get_households(self, per_page: int = 100) -> List[Dict]:
        """Get all households."""
        data = self._get("households", {"per_page": per_page})
        return data.get("data", [])

    def get_household(self, household_id: str) -> Dict:
        """Get a specific household."""
        return self._get(f"households/{household_id}")

    def get_household_members(self, household_id: str) -> List[Dict]:
        """Get people in a household."""
        data = self._get(f"households/{household_id}/people")
        return data.get("data", [])
