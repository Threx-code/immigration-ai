from typing import Optional
import requests
import logging

logger = logging.getLogger("django")

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url


    def get(self, endpoint: str, headers: Optional[dict] = None, params: Optional[str] = None):
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while making GET request to {endpoint}: {e}")
            return None

    def post(self, endpoint, data, headers:Optional[dict] = None):
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while making POST request to {endpoint}: {e}")
            return None

    def put(self, endpoint, data, headers: Optional[dict]=None):
        try:
            response = requests.put(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while making PUT request to {endpoint}: {e}")
            return None

    def delete(self, endpoint, headers=None):
        try:
            response = requests.delete(
                f"{self.base_url}{endpoint}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while making DELETE request to {endpoint}: {e}")
            return None