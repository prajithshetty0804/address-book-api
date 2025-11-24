from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")
    description: Optional[str] = Field(None, description="Extra notes about the address")

class AddressCreate(AddressBase):
    """Schema used when a user creates or updates an address."""
    pass

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
