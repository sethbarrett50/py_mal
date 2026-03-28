from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field


class PacketType(IntEnum):
    FRAME = 1
    INPUT = 2


class InputEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    event_type: str = Field(..., alias='type')
    x: int | None = None
    y: int | None = None
    button: str = 'left'
    key_code: str | None = None
