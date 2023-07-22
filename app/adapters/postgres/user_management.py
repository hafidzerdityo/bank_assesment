import api.models.db_model as db_model
from db.database_config import database
from api.schemas.user_management import RequestDaftar, ResponseDaftar
from adapters.postgres.utils import generate_unique_account_number

################## Start of post_user services ##################

async def check_user(no_hp: str,  nik: str):
    query = db_model.Nasabah.select().where(
    (db_model.Nasabah.c.no_hp == no_hp) |
    (db_model.Nasabah.c.nik == nik)
    )
    user_exist = await database.fetch_one(query)
    return user_exist

async def create_user(req_payload:RequestDaftar) -> ResponseDaftar:
    get_rekening = await generate_unique_account_number()
    get_saldo: int  = 0 
    query = db_model.Nasabah.insert().values(
        no_rekening = get_rekening,
        no_hp = req_payload.no_hp,
        nama = req_payload.nama,
        nik = req_payload.nik,
        saldo = get_saldo
    )
    await database.execute(query)
    return ResponseDaftar(
        no_rekening = get_rekening
    )

################## End of post_user services ##################