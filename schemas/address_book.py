from pydantic import BaseModel, Field, validator
from typing import Optional, List


class CreateAddress(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class AllAddress(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    is_active: bool = Field(default=True)
    is_disabled: bool = Field(default=False)
    created_by_ip: str


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = Field(..., ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(..., ge=-180.0, le=180.0)

    @validator("latitude")
    def latitude_must_be_valid(cls, v):
        """
        validate latitude
        """
        if v < -90.0 or v > 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @validator("longitude")
    def longitude_must_be_valid(cls, v):
        """
        validate longitude
        """
        if v < -180.0 or v > 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        return v


class ReturnResponseSuccess(BaseModel):
    status: int = Field(default=404, examples=[404, 400])
    detail: str = Field(default="Success", examples=["Success"])
    data: List[AllAddress] = Field(default=[])