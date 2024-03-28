from fastapi import HTTPException
from models import Address
from sqlalchemy.orm import session
from sqlalchemy import and_
from math import radians, sin, cos, sqrt, atan2

from schemas.address_book import CreateAddress, ReturnResponseSuccess, AllAddress, AddressUpdate


async def get_addresses(db: session, ip_address:str):
    all_addresses = db.query(Address).filter(and_(Address.is_active == True, Address.created_by_ip == ip_address)).all()
    serialized_addresses = [AllAddress(**address.__dict__) for address in all_addresses]
    return ReturnResponseSuccess(status=200, detail="Address Book Fetched Successfully",
                                 data=serialized_addresses)


async def create_address(message_data:CreateAddress, db:session, ip_address:str):
    message_data = message_data.model_dump()
    message_data['created_by_ip'] = ip_address
    new_message = Address(**message_data)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return ReturnResponseSuccess(status=201, detail="Address Created Successfully",
                                 data=[AllAddress(**new_message.__dict__)])


async def get_single_address(id:int, db:session, ip_address:str):
    address = db.query(Address).filter(and_(Address.id == id, Address.is_active == True))
    if not address.first():
        raise HTTPException(status_code=404, detail="Requested Address Book Not Available")
    if address.first().created_by_ip != ip_address:
        raise HTTPException(status_code=401, detail="You Are Not Authorized to Fetch the Address")
    
    return ReturnResponseSuccess(status=200, detail="Address Fetched Successfully",
                                 data=[AllAddress(**address.first().__dict__)])


async def edit_address(id:int, message_data:AddressUpdate, db:session, ip_address:str):
    message_data = message_data.model_dump()
    address = db.query(Address).filter(and_(Address.id == id, Address.is_active == True))
    if not address.first():
        raise HTTPException(status_code=404, detail="Requested Address Book Not Available")
    if address.first().created_by_ip != ip_address:
        raise HTTPException(status_code=401, detail="You Are Not Authorized to Update the Address")
    
    address.update(message_data)
    db.commit()
    return ReturnResponseSuccess(status=200, detail="Address Created Successfully",
                                 data=[AllAddress(**address.first().__dict__)])


async def disable_address(id:int, db:session, ip_address:str):
    address = db.query(Address).filter(and_(Address.id == id, Address.is_active == True))
    if not address.first():
        raise HTTPException(status_code=404, detail="Requested Address Book Not Available")
    if address.first().created_by_ip != ip_address:
        raise HTTPException(status_code=403, detail="You Are Not Authorized to Disable the Address")
    
    address_obj = address.first()
    address_obj.is_active = False
    address_obj.is_disabled = True
    db.commit()
    
    return ReturnResponseSuccess(status=200, detail="Address Disabled Successfully",
                                 data=[])


async def delete_address(id:int, db:session, ip_address:str):
    address = db.query(Address).filter(and_(Address.id == id, Address.is_active == True))
    if not address.first():
        raise HTTPException(status_code=404, detail="Requested Address Book Not Available")
    if address.first().created_by_ip != ip_address:
        raise HTTPException(status_code=403, detail="You Are Not Authorized to Delete the Address")
    
    # address.delete(synchronize_session=False)
    address.delete(synchronize_session=False)
    db.commit()
    
    return ReturnResponseSuccess(status=204, detail="Address Permanently Deleted",
                                 data=[])


async def calculate_distance(lat1, lon1, lat2, lon2):
    # total radius
    R = 6371.0

    # value in radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


async def get_addresses_nearby(id:int, kms:int, db:session, ip_address:str):
    address = db.query(Address).filter(and_(Address.id == id, Address.is_active == True))
    if not address.first():
        raise HTTPException(status_code=404, detail="Requested Address Book Not Available")
    if address.first().created_by_ip != ip_address:
        raise HTTPException(status_code=403, detail="You Are Not Authorized to Delete the Address")
    
    target_latitude = address.first().latitude
    target_longitude = address.first().longitude
    # Retrieve all addresses from the database
    all_addresses = db.query(Address).filter(Address.is_active == True).all()
    nearby_addresses = []
    
    for address in all_addresses:
        dist = await calculate_distance(target_latitude, target_longitude, address.latitude, address.longitude)
        if dist <= kms:
            nearby_addresses.append(address)

    return nearby_addresses