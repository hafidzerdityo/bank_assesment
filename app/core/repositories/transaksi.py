import core.models.db_model as db_model
from db.database_config import database
import core.schemas.transaksi as transaksi_schemas
from typing import List, Dict
import core.repositories.utils as utils

async def create_tabung(create_tabung_payload: transaksi_schemas.RequestTabung) -> transaksi_schemas.ResponseTabung:
    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == create_tabung_payload.no_rekening
    )
    user_exist = await database.fetch_one(query)
    if not user_exist:
        raise Exception("Nomor Rekening Tidak Diketahui")
    
    saldo = round(float(create_tabung_payload.nominal),2)
    if user_exist.saldo is not None:
        saldo += round(float(user_exist.saldo),2)

    query = db_model.Nasabah.update().values(
        saldo=saldo
    ).where(
        db_model.Nasabah.c.no_rekening == create_tabung_payload.no_rekening
    )

    await database.execute(query)

    query = db_model.Transaksi.insert().values(
        kode_transaksi='C',
        waktu=utils.get_current_datetime(),
        no_rekening=user_exist.no_rekening,
        nominal=float(create_tabung_payload.nominal)
    )

    await database.execute(query)

    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == create_tabung_payload.no_rekening
    )
    get_latest_saldo = await database.fetch_one(query)

    return transaksi_schemas.ResponseTabung(
        saldo= round(float(get_latest_saldo.saldo),2)
    )

async def create_tarik(create_tarik_payload: transaksi_schemas.RequestTarik) -> transaksi_schemas.ResponseTarik:
    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == create_tarik_payload.no_rekening
    )
    user_exist = await database.fetch_one(query)
    if not user_exist:
        raise Exception("Nomor Rekening Tidak Diketahui")
    
    saldo = round(float(create_tarik_payload.nominal),2)
    user_exist.saldo = round(float(user_exist.saldo),2)

    if user_exist.saldo is not None:
        user_exist.saldo -= saldo

    if user_exist.saldo < 0 :
        raise Exception("Saldo Tidak Cukup")

    query = db_model.Nasabah.update().values(
        saldo=user_exist.saldo
    ).where(
        db_model.Nasabah.c.no_rekening == create_tarik_payload.no_rekening
    )

    await database.execute(query)

    query = db_model.Transaksi.insert().values(
        kode_transaksi='D',
        waktu=utils.get_current_datetime(),
        no_rekening=user_exist.no_rekening,
        nominal=float(create_tarik_payload.nominal)
    )

    await database.execute(query)

    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == create_tarik_payload.no_rekening
    )
    get_latest_saldo = await database.fetch_one(query)

    return transaksi_schemas.ResponseTabung(
        saldo= round(float(get_latest_saldo.saldo),2)
    )

async def get_saldo(get_saldo_payload: str) -> transaksi_schemas.ResponseSaldo:
    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == get_saldo_payload
    )
    get_latest_saldo = await database.fetch_one(query)
    if not get_latest_saldo:
        raise Exception('No Rekening Tidak Diketahui')

    return transaksi_schemas.ResponseSaldo(
        saldo= round(float(get_latest_saldo.saldo),2)
    )

from typing import List

async def get_mutasi(get_mutasi_payload: str) -> List[transaksi_schemas.ResponseMutasi]:
    query = db_model.Nasabah.select().where(
        db_model.Nasabah.c.no_rekening == get_mutasi_payload
    )
    check_rekening = await database.fetch_one(query)
    if not check_rekening:
        raise Exception('No Rekening Tidak Diketahui')
    
    query = db_model.Transaksi.select().where(
        db_model.Transaksi.c.no_rekening == get_mutasi_payload
    )
    mutasi_data = await database.fetch_all(query)

    response_list = []
    for row in mutasi_data:
        response_list.append(
            transaksi_schemas.ResponseMutasi(
                kode_transaksi=row.kode_transaksi,
                waktu=row.waktu.strftime('%Y-%m-%d %H:%M:%S'),
                nominal= float(round(row.nominal,2))
            )
        )

    return response_list

