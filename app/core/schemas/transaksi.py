from typing import Optional, List,Dict, Union
from pydantic import BaseModel, StrictFloat, StrictStr, StrictInt, StrictBool, validator,constr, confloat
from datetime import date


class RequestTabung(BaseModel):
    no_rekening: constr(max_length=255)
    nominal: Union[StrictFloat, StrictInt]

    @validator('nominal')
    def validate_nominal(cls, value):
        if value <= 0:
            raise ValueError('Nominal should be a positive number greater than 0')
        return value
    
class ResponseTabung(BaseModel):
    saldo: StrictFloat
    class Config:
        orm_mode = True

class RequestTarik(BaseModel):
    no_rekening: constr(max_length=255)
    nominal: Union[StrictFloat, StrictInt]

    @validator('nominal')
    def validate_nominal(cls, value):
        if value <= 0:
            raise ValueError('Nominal should be a positive number greater than 0')
        return value

class ResponseTarik(BaseModel):
    saldo: StrictFloat
    class Config:
        orm_mode = True

class RequestSaldo(BaseModel):
    no_rekening: constr(max_length=255)

class ResponseSaldo(BaseModel):
    saldo: StrictFloat
    class Config:
        orm_mode = True

class RequestMutasi(BaseModel):
    no_rekening: constr(max_length=255)
    
class ResponseMutasi(BaseModel):
    kode_transaksi: constr(max_length=255)
    waktu: constr(max_length=255)
    nominal: StrictFloat
    class Config:
        orm_mode = True