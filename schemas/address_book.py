from pydantic import BaseModel, Field, validator, conint
from typing import Optional, List
from datetime import datetime


class CreateAddress(BaseModel):
    street: str
    city: str
    state: str
    postal_code: int = Field(..., ge=100000, le=999999)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class AllAddress(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: int = Field(None, ge=100000, le=999999)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    is_active: bool = Field(default=True)
    is_disabled: bool = Field(default=False)
    created_by_ip: str
    created_at: datetime
    modified_at: datetime


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[int] = Field(None, ge=100000, le=999999)
    latitude: Optional[float] = Field(..., ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(..., ge=-180.0, le=180.0)


class ReturnResponseSuccess(BaseModel):
    status: int = Field(default=404, examples=[404, 400])
    detail: str = Field(default="Success", examples=["Success"])
    data: List[AllAddress]
