from fastapi import FastAPI, HTTPException, Query
from typing import List
import math

from models import Address, AddressCreate
from database import (
    initialize_database,
    insert_address,
    fetch_address,
    fetch_all_addresses,
    update_address,
    delete_address,
)


app = FastAPI(
    title="Address Book API",
    description="API for storing and retrieving addresses based on coordinates.",
    version="1.0",
)


# Create table automatically when the application starts
initialize_database()


def convert_row_to_model(row) -> Address:
    return Address(
        id=row["id"],
        name=row["name"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        description=row["description"],
    )


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Returns distance between two coordinates in kilometers using Haversine formula."""
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@app.post("/addresses", response_model=Address)
def create_address(address: AddressCreate):
    new_id = insert_address(
        address.name,
        address.latitude,
        address.longitude,
        address.description,
    )
    row = fetch_address(new_id)
    return convert_row_to_model(row)


@app.get("/addresses", response_model=List[Address])
def get_all():
    rows = fetch_all_addresses()
    return [convert_row_to_model(r) for r in rows]

@app.get("/addresses/search", response_model=List[Address])
def search_nearby(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
):
    rows = fetch_all_addresses()
    result = []
    for row in rows:
        dist = calculate_distance(
            latitude,
            longitude,
            row["latitude"],
            row["longitude"],
        )
        if dist <= distance_km:
            result.append(convert_row_to_model(row))
    return result


@app.get("/addresses/{address_id}", response_model=Address)
def get_one(address_id: int):
    row = fetch_address(address_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return convert_row_to_model(row)


@app.put("/addresses/{address_id}", response_model=Address)
def update(address_id: int, data: AddressCreate):
    updated = update_address(
        address_id,
        data.name,
        data.latitude,
        data.longitude,
        data.description,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    row = fetch_address(address_id)
    return convert_row_to_model(row)


@app.delete("/addresses/{address_id}")
def delete(address_id: int):
    deleted = delete_address(address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address removed successfully"}


