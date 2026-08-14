"""SIte activation gateway."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def status():
    return {
        "service": "SIte",
        "network": "333 Network",
        "state": "frontend-ready",
        "backend": "pending",
        "purpose": "site-builder",
        "domainHosting": "WEAL-planned",
    }
