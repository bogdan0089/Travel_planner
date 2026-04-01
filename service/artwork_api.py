import json
import httpx
import redis.asyncio as aioredis
from core.cfg import settings


class ArtworkAPIService:
    def __init__(self):
        self._redis: aioredis.Redis | None = None


    async def _get_redis(self) -> aioredis.Redis | None:
        if not settings.REDIS_URL:
            return None
        if self._redis is None:
            try:
                self._redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
                await self._redis.ping()
            except Exception:
                self._redis = None
        return self._redis

    async def get_artwork(self, artwork_id: int) -> dict | None:
        cache_key = f"artwork:{artwork_id}"
        redis = await self._get_redis()
        if redis:
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.ARTIC_BASE_URL}/artworks/{artwork_id}",
                params={"fields": "id,title,artist_display,image_id"},
            )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json().get("data")
        if data and redis:
            await redis.setex(cache_key, settings.ARTIC_CACHE_TTL, json.dumps(data))
        return data

    def build_image_url(self, image_id: str | None) -> str | None:
        if not image_id:
            return None
        return f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"


artwork_api = ArtworkAPIService()
