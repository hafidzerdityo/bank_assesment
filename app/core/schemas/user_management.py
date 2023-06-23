from typing import Optional, List,Dict, Union
from pydantic import BaseModel, StrictFloat, StrictStr, StrictInt, StrictBool, validator,constr
from datetime import date


class RequestDaftar(BaseModel):
    nama: constr(max_length=255)
    nik: constr(max_length=255)
    no_hp: constr(max_length=255)
    @validator('nik')
    def validate_nik(cls, value):
        if not value.isdigit():
            raise ValueError('NIK should only contain numeric characters')
        return value

    @validator('no_hp')
    def validate_no_hp(cls, value):
        if not value.isdigit():
            raise ValueError('No. HP should only contain numeric characters')
        return value

class ResponseDaftar(BaseModel):
    no_rekening: constr(max_length=255)
    class Config:
        orm_mode = True