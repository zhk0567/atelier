from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import site_context, templates
from app.travel_catalog import get_travel_trip, load_travel_trips

router = APIRouter()


@router.get("/travel", response_class=HTMLResponse)
async def travel_index(request: Request):
    trips = load_travel_trips()
    return templates.TemplateResponse(
        request=request,
        name="travel_index.html",
        context={
            **site_context(),
            "trips": trips,
            "trip_count": len(trips),
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/travel/{trip_id}", response_class=HTMLResponse)
async def travel_trip(request: Request, trip_id: str):
    trip = get_travel_trip(trip_id)
    if not trip:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="travel_trip.html",
        context={
            **site_context(),
            **trip,
            "item_count": trip["photo_count"],
        },
        headers=HTML_CACHE_HEADERS,
    )
