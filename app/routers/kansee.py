"""KANSEE activation gateway.

Phase 1 intentionally reports capability state without pretending that meeting
signaling is already connected to the backend.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def status():
    return {
        "service": "KANSEE",
        "network": "333 Network",
        "state": "frontend-ready",
        "backend": "pending",
        "purpose": "meeting-rooms",
    }
