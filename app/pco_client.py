"""
Planning Center API Client
Handles authentication and data retrieval from Planning Center Services API.
"""

import os
import requests
from base64 import b64encode
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class PCOClient:
    """Client for interacting with Planning Center Services API."""

    BASE_URL = "https://api.planningcenteronline.com/services/v2"

    def __init__(self, app_id: str = None, secret: str = None):
        self.app_id = app_id or os.getenv("PCO_APP_ID")
        self.secret = secret or os.getenv("PCO_SECRET")

        if not self.app_id or not self.secret:
            raise ValueError(
                "PCO_APP_ID and PCO_SECRET must be set in environment or .env file"
            )

        self._session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self):
        """Set Basic Auth header using app_id and secret."""
        credentials = b64encode(f"{self.app_id}:{self.secret}".encode()).decode()
        self._session.headers.update({"Authorization": f"Basic {credentials}"})

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the PCO API."""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_service_types(self) -> List[Dict]:
        """Get all service types (e.g., Sunday Worship, Children's Check-in)."""
        data = self._get("service_types")
        return data.get("data", [])

    def get_service_type_by_name(self, name: str) -> Optional[Dict]:
        """Find a service type by name (case-insensitive)."""
        service_types = self.get_service_types()
        for st in service_types:
            if st["attributes"]["name"].lower() == name.lower():
                return st
        return None

    def get_plan_times(self, service_type_id: str, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Get plan times (service instances) for a service type.

        Args:
            service_type_id: The service type ID
            start_date: Start date filter (ISO format: YYYY-MM-DD)
            end_date: End date filter (ISO format: YYYY-MM-DD)
        """
        params = {
            "where[dates]": f"{start_date}/{end_date}" if start_date and end_date else None,
            "per_page": 100,
        }
        params = {k: v for k, v in params.items() if v is not None}

        data = self._get(f"service_types/{service_type_id}/plan_times", params)
        return data.get("data", [])

    def get_headcounts(self, plan_time_id: str) -> List[Dict]:
        """Get headcount data for a specific plan time."""
        data = self._get(f"plan_times/{plan_time_id}/head_counts")
        return data.get("data", [])

    def get_aggregated_attendance(
        self,
        service_type_ids: List[str],
        start_date: str,
        end_date: str,
    ) -> Dict[str, int]:
        """
        Get aggregated attendance across multiple service types for a date range.

        Returns:
            Dict mapping date strings to total attendance counts
        """
        attendance = {}

        for st_id in service_type_ids:
            plan_times = self.get_plan_times(st_id, start_date, end_date)

            for pt in plan_times:
                date_str = pt["attributes"]["starts_at"][:10]  # Extract date portion
                headcounts = self.get_headcounts(pt["id"])

                total = sum(hc["attributes"]["count"] for hc in headcounts)

                if date_str not in attendance:
                    attendance[date_str] = 0
                attendance[date_str] += total

        return attendance

    def get_year_over_year_comparison(
        self,
        service_type_ids: List[str],
        reference_date: str,
        lookback_days: int = 90,
    ) -> Dict[str, Dict[str, int]]:
        """
        Get year-over-year attendance comparison.

        Args:
            service_type_ids: List of service type IDs to include
            reference_date: The reference date (usually today)
            lookback_days: How many days back to compare

        Returns:
            Dict with 'current' and 'previous_year' attendance data
        """
        ref_date = datetime.fromisoformat(reference_date)
        start_current = (ref_date - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        end_current = ref_date.strftime("%Y-%m-%d")

        prev_year_start = (ref_date - timedelta(days=lookback_days + 365)).strftime("%Y-%m-%d")
        prev_year_end = (ref_date - timedelta(days=365)).strftime("%Y-%m-%d")

        current_attendance = self.get_aggregated_attendance(
            service_type_ids, start_current, end_current
        )

        previous_attendance = self.get_aggregated_attendance(
            service_type_ids, prev_year_start, prev_year_end
        )

        # Shift previous year dates forward by 365 days for comparison
        shifted_previous = {}
        for date_str, count in previous_attendance.items():
            date_obj = datetime.fromisoformat(date_str)
            shifted_date = (date_obj + timedelta(days=365)).strftime("%Y-%m-%d")
            shifted_previous[shifted_date] = count

        return {
            "current": current_attendance,
            "previous_year": shifted_previous,
        }
