import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class PexelsService:
    BASE_URL = "https://api.pexels.com/v1"
    CACHE_TIMEOUT = 300  # 5 minutes

    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY

    def _get_cache_key(self, endpoint, params):
        # Create unique cache key based on endpoint and parameters
        param_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"pexels_{endpoint}_{param_string}"

    def _make_request(self, endpoint, params=None):
        cache_key = self._get_cache_key(endpoint, params or {})
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return cached_response

        try:
            url = f"{self.BASE_URL}/{endpoint}"
            headers = {
                "Authorization": self.api_key  # Just the API key value
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            cache.set(cache_key, data, self.CACHE_TIMEOUT)
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Pexels API error: {str(e)}")
            raise

    def search_photos(self, query, page=1, per_page=15, orientation=None, size=None, color=None):
        params = {
            "query": query,
            "page": page,
            "per_page": min(per_page, 80)  # Max allowed by Pexels is 80
        }
        
        if orientation:
            params["orientation"] = orientation
        if size:
            params["size"] = size
        if color:
            params["color"] = color

        return self._make_request("search", params)

    def get_curated_photos(self, page=1, per_page=15):
        params = {
            "page": page,
            "per_page": min(per_page, 80)
        }
        return self._make_request("curated", params)

    def get_photo(self, photo_id):
        return self._make_request(f"photos/{photo_id}")
