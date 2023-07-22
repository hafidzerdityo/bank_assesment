import api.models.db_model as db_model
from db.database_config import database
from api.schemas.transaksi import RequestTabung, RequestTarik, ResponseMutasi, ResponseSaldo ,ResponseTabung, ResponseTarik
from typing import List, Dict
import adapters.postgres.utils as utils
from sqlalchemy import select



async def read_latest_saldo(no_rekening: str) -> ResponseSaldo:
    query = select([db_model.Nasabah.c.saldo]).where(
        db_model.Nasabah.c.no_rekening == no_rekening
    )
    latest_saldo = await database.fetch_one(query)
    formatted_latest_saldo = round(float(latest_saldo['saldo']),2)
    return ResponseSaldo(
        saldo = formatted_latest_saldo if latest_saldo else None
    )

async def check_exist_by_no_rekening(no_rekening: str):
    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == no_rekening
    )
    user_exist = await database.fetch_one(query)
    return user_exist


async def insert_mutasi(kode_transaksi, no_rekening, nominal):
    # if nominal > 10:
    #     raise Exception('Error, reason: more than 10')
    query = db_model.Transaksi.insert().values(
    kode_transaksi=kode_transaksi,
    waktu = utils.get_current_datetime(),
    no_rekening=no_rekening,
    nominal=float(nominal)
    )
    await database.execute(query)
    


async def create_tabung(req_payload: RequestTabung, user_exist) -> ResponseTabung:
    saldo = round(float(req_payload.nominal),2)
    if user_exist.saldo is not None:
        saldo += round(float(user_exist.saldo),2)
    query = db_model.Nasabah.update().values(
        saldo=saldo
    ).where(
        db_model.Nasabah.c.no_rekening == req_payload.no_rekening
    )
    await database.execute(query)

    await insert_mutasi(
        kode_transaksi='C',
        no_rekening= user_exist.no_rekening,
        nominal= req_payload.nominal
    )

    get_latest_saldo = await check_exist_by_no_rekening(req_payload.no_rekening)

    return ResponseTabung(
        saldo= round(float(get_latest_saldo.saldo),2)
    )

async def create_tarik(req_payload: RequestTarik, user_exist) -> ResponseTarik:
    saldo = round(float(req_payload.nominal),2)
    user_exist.saldo = round(float(user_exist.saldo),2)

    if user_exist.saldo is not None:
        user_exist.saldo -= saldo

    if user_exist.saldo < 0 :
        raise Exception("Saldo Tidak Cukup")

    query = db_model.Nasabah.update().values(
        saldo=user_exist.saldo
    ).where(
        db_model.Nasabah.c.no_rekening == req_payload.no_rekening
    )

    await database.execute(query)

    await insert_mutasi(
        kode_transaksi='D',
        no_rekening= user_exist.no_rekening,
        nominal= req_payload.nominal
    )

    get_latest_saldo = await check_exist_by_no_rekening(req_payload.no_rekening)

    return ResponseTabung(
        saldo= round(float(get_latest_saldo.saldo),2)
    )




async def read_mutasi(get_mutasi_payload: str) -> List[ResponseMutasi]:

    query = db_model.Transaksi.select().where(
        db_model.Transaksi.c.no_rekening == get_mutasi_payload
    )
    mutasi_data = await database.fetch_all(query)

    response_list = []
    for row in mutasi_data:
        response_list.append(
            ResponseMutasi(
                kode_transaksi=row.kode_transaksi,
                waktu=row.waktu.strftime('%Y-%m-%d %H:%M:%S'),
                nominal= float(round(row.nominal,2))
            )
        )

    return response_list

