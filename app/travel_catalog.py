"""Personal travel trips and photo galleries."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.config import ATELIER_ROOT
from app.media_derivatives import ensure_travel_derivatives

TRAVEL_DATA_DIR = ATELIER_ROOT / "data" / "travel"
TRIPS_MANIFEST = TRAVEL_DATA_DIR / "trips.json"
UPLOAD_URL_PREFIX = "/static/uploads/travel"


@lru_cache(maxsize=1)
def load_travel_trips() -> list[dict]:
    if not TRIPS_MANIFEST.is_file():
        return []
    try:
        raw = json.loads(TRIPS_MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    trips = raw.get("trips") if isinstance(raw, dict) else raw
    if not isinstance(trips, list):
        return []
    out: list[dict] = []
    for trip in trips:
        if not isinstance(trip, dict) or not trip.get("id"):
            continue
        enriched = _enrich_trip(trip)
        if enriched.get("photos"):
            out.append(enriched)
    return out


def get_travel_trip(trip_id: str) -> dict | None:
    for trip in load_travel_trips():
        if trip["id"] == trip_id:
            return trip
    return None


def clear_travel_cache() -> None:
    load_travel_trips.cache_clear()


def _enrich_trip(trip: dict) -> dict:
    trip_id = str(trip["id"])
    base_dir = ATELIER_ROOT / "static" / "uploads" / "travel" / trip_id
    photos_in: list[dict] = trip.get("photos") or []
    photos: list[dict] = []
    for i, photo in enumerate(photos_in, start=1):
        if not isinstance(photo, dict):
            continue
        filename = photo.get("file") or ""
        if not filename:
            continue
        path = base_dir / filename
        if not path.is_file():
            continue
        thumb_name, web_name = ensure_travel_derivatives(base_dir, filename)
        orig_url = f"{UPLOAD_URL_PREFIX}/{trip_id}/{filename}"
        thumb_url = (
            f"{UPLOAD_URL_PREFIX}/{trip_id}/{thumb_name}"
            if thumb_name
            else orig_url
        )
        display_url = (
            f"{UPLOAD_URL_PREFIX}/{trip_id}/{web_name}" if web_name else orig_url
        )
        photos.append({
            "id": photo.get("id") or f"{i:02d}",
            "file": filename,
            "title": photo.get("title") or f"照片 {i:02d}",
            "meta": photo.get("meta", ""),
            "thumb_url": thumb_url,
            "image_url": display_url,
        })
    cover_file = trip.get("cover") or (photos[0]["file"] if photos else "")
    cover_url = ""
    if cover_file and (base_dir / cover_file).is_file():
        thumb_name, _ = ensure_travel_derivatives(base_dir, cover_file)
        if thumb_name:
            cover_url = f"{UPLOAD_URL_PREFIX}/{trip_id}/{thumb_name}"
        else:
            cover_url = f"{UPLOAD_URL_PREFIX}/{trip_id}/{cover_file}"
    elif photos:
        cover_url = photos[0].get("thumb_url") or photos[0]["image_url"]
    return {
        "id": trip_id,
        "title": trip.get("title") or trip_id,
        "summary": trip.get("summary", ""),
        "date": trip.get("date", ""),
        "cover_url": cover_url,
        "photo_count": len(photos),
        "photos": photos,
        "url": f"/travel/{trip_id}",
    }
