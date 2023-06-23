import core.models.db_model as db_model
from db.database_config import database
import core.schemas.user_management as user_management_schemas
from typing import List, Dict
import core.repositories.utils as utils

async def create_user(create_user_payload: user_management_schemas.RequestDaftar) -> user_management_schemas.ResponseDaftar:
    query = db_model.Nasabah.select().where(
    (db_model.Nasabah.c.no_hp == create_user_payload.no_hp) |
    (db_model.Nasabah.c.nik == create_user_payload.nik)
    )
    user_exist = await database.fetch_one(query)
    if user_exist:
        raise Exception("Nomor HP atau NIK Sudah Terdaftar")
    
    get_rekening = await utils.generate_unique_account_number()
    get_saldo: int  = 0 
    query = db_model.Nasabah.insert().values(
        no_rekening = get_rekening,
        no_hp = create_user_payload.no_hp,
        nama = create_user_payload.nama,
        nik = create_user_payload.nik,
        saldo = get_saldo
    )
    await database.execute(query)
    return user_management_schemas.ResponseDaftar(
        no_rekening = get_rekening
    )