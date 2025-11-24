# Address Book API – FastAPI

This project is a simple Address Book API built using FastAPI.  
The goal of the app is to store address information along with their coordinates and allow users to search nearby locations based on distance.

The API supports all CRUD operations and also has a custom search feature using the Haversine distance formula.

## Tech Stack Used
- Python
- FastAPI
- SQLite
- Pydantic (for model validation)
- Uvicorn (for running the server)

## Features
- Add a new address with latitude and longitude
- Get the list of all saved addresses
- Get one address by its ID
- Update an existing address
- Delete an address
- Search for nearby addresses by passing latitude, longitude and distance (km)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /addresses | Create a new address |
| GET | /addresses | Fetch all addresses |
| GET | /addresses/{address_id} | Fetch single address by ID |
| PUT | /addresses/{address_id} | Update an address |
| DELETE | /addresses/{address_id} | Delete an address |
| GET | /addresses/search | Search nearby addresses |

## Sample JSON for POST request
```json
{
  "name": "Gachibowli",
  "latitude": 17.4401,
  "longitude": 78.3489,
  "description": "Location Gachibowli"
}
```
