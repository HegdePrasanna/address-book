from pydantic import BaseModel, Field
from typing import List


class ReturnResponseFailure(BaseModel):
    status: int = Field(default=404, examples=[404, 400])
    detail: str = Field(default="Requested Resource Not Found", examples=["Requested Resource Not Found"])
    data: List = Field(default=[])


class BadRequest(BaseModel):
    status: int = Field(default=400, examples=[400])
    detail: str = Field(default="Invalid Request Body", examples=["Invalid Request Body"])
    data: List = Field(default=[])


class Unauthorised(BaseModel):
    status: int = Field(default=401, examples=[401])
    detail: str = Field(default="Not Authorised to Perform This Action",
                        examples=["Not Authorised to Perform This Action"])
    data: List = Field(default=[])
