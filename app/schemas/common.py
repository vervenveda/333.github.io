"""Shared API schemas."""

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class MessageResponse(ApiModel):
    message: str
