"""Bazaar Art Live social-feed gateway backed by encrypted OHMIC persistence."""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field

from app.dependencies.sovereign_authentication import SovereignMember, get_current_sovereign_member
from app.services.ohmic_bazaar_service import add_comment, bazaar_status, create_post, delete_post, get_post, list_feed, set_reaction

router = APIRouter()

class MediaMetadata(BaseModel):
    id: str = Field(min_length=1, max_length=128)
    type: str = Field(min_length=1, max_length=120)
    alt: str | None = Field(default=None, max_length=500)
    storage: str = Field(default="local-first", max_length=40)

class PostCreate(BaseModel):
    type: Literal["post", "reel"] = "post"
    text: str = Field(default="", max_length=10000)
    audience: Literal["public", "members", "private"] = "members"
    location: str | None = Field(default=None, max_length=200)
    tags: list[str] = Field(default_factory=list, max_length=20)
    media: list[MediaMetadata] = Field(default_factory=list, max_length=8)

class ReactionSet(BaseModel):
    reaction: Literal["", "like", "love", "fire", "applause"] = ""

class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=3000)

@router.get("/status")
async def status_route() -> dict[str, Any]:
    upstream = await bazaar_status()
    return {
        "service": "Bazaar Art",
        "network": "333 Network",
        "state": str(upstream.get("state") or "backend-ready"),
        "backend": "OHMIC Foundry",
        "purpose": "social-media-feed",
        "encryptedPersistence": bool((upstream.get("vault") or {}).get("encryptedAtRest")),
        "media": "local-first-metadata-only",
        "counts": upstream.get("counts") or {},
    }

@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post_route(payload: PostCreate, member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await create_post(member_id=member.id, post=payload.model_dump(mode="json"))

@router.get("/feed")
async def feed_route(limit: int = Query(default=50, ge=1, le=100), before: str | None = Query(default=None, max_length=100), member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await list_feed(member_id=member.id, limit=limit, before=before)

@router.get("/posts/{post_id}")
async def get_post_route(post_id: str, member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await get_post(member_id=member.id, post_id=post_id)

@router.put("/posts/{post_id}/reaction")
async def reaction_route(post_id: str, payload: ReactionSet, member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await set_reaction(member_id=member.id, post_id=post_id, reaction=payload.reaction)

@router.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def comment_route(post_id: str, payload: CommentCreate, member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await add_comment(member_id=member.id, post_id=post_id, text=payload.text)

@router.delete("/posts/{post_id}")
async def delete_post_route(post_id: str, member: SovereignMember = Depends(get_current_sovereign_member)) -> dict[str, Any]:
    return await delete_post(member_id=member.id, post_id=post_id)
