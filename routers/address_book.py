from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from services.address_book import (create_address, get_addresses, edit_address,
                                   disable_address, delete_address, get_single_address, get_addresses_nearby)
from services.generic import get_client_ip
from schemas.address_book import CreateAddress, ReturnResponseSuccess, AddressUpdate
from schemas.generic import ReturnResponseFailure, BadRequest, Unauthorised

addr_router = APIRouter(
    tags=["Address Book"], prefix="/address"
)


@addr_router.get("/list", responses={404: {"model": ReturnResponseFailure}, 200: {"model": ReturnResponseSuccess}})
async def get_all_addresses(db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Get All Active Addresses
    """
    address = await get_addresses(db, ip_address)
    return address


@addr_router.post("/create", responses={400: {"model": BadRequest}, 401: {"model": Unauthorised},
                                        200: {"model": ReturnResponseSuccess}})
async def create_new_address(address: CreateAddress, db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Create New Address
    """
    address = await create_address(address, db, ip_address)
    return address


@addr_router.get("/get/{id}", responses={400: {"model": BadRequest}, 401: {"model": Unauthorised},
                                         200: {"model": ReturnResponseSuccess}})
async def get_address_by_id(id: int, db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Get Address By ID
    """
    address = await get_single_address(id, db, ip_address)
    return address


@addr_router.put("/update/{id}", responses={400: {"model": BadRequest}, 401: {"model": Unauthorised},
                                            200: {"model": ReturnResponseSuccess}})
async def update_address_by_id(id: int, address: AddressUpdate, db: Session = Depends(get_db),
                               ip_address=Depends(get_client_ip)):
    """
    Update the Existing Address
    """
    address = await edit_address(id, address, db, ip_address)
    return address


@addr_router.put("/disable/{id}",
                 responses={404: {"model": ReturnResponseFailure}, 200: {"model": ReturnResponseSuccess}})
async def disable_address_by_id(id: int, db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Disable the Existing Address
    """
    address = await disable_address(id, db, ip_address)
    return address


@addr_router.delete("/delete/{id}",
                    responses={404: {"model": ReturnResponseFailure}, 200: {"model": ReturnResponseSuccess}})
async def delete_address_by_id(id: int, db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Permanently Delete the Existing Address
    """
    address = await delete_address(id, db, ip_address)
    return address


near_by_locations = APIRouter(
    tags=["NearBy Location"], prefix="/nearby"
)


@near_by_locations.get("id/{id}/distance/{kms}",
                       responses={404: {"model": ReturnResponseFailure}, 200: {"model": ReturnResponseSuccess}})
async def get_nearby_location(id: int, kms: int, db: Session = Depends(get_db), ip_address=Depends(get_client_ip)):
    """
    Get NearBy Addresses Stored in Address Book
    """
    address = await get_addresses_nearby(id, kms, db, ip_address)
    return address
