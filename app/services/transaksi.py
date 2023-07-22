from api.schemas.transaksi import RequestTabung, ResponseTabung, RequestTarik, ResponseTarik, ResponseSaldo, ResponseMutasi
from db.database_config import database
from adapters.postgres.transaksi import check_exist_by_no_rekening, create_tabung, create_tarik, read_latest_saldo, read_mutasi

from api.routers.log import logger

async def post_tabung(req_payload: RequestTabung) -> ResponseTabung:
    async with database.transaction():
        user_exist = await check_exist_by_no_rekening(req_payload.no_rekening)
        if not user_exist:
            remark = "Nomor Rekening Tidak Diketahui"
            logger.error(remark) 
            raise Exception(remark)
        latest_saldo = await create_tabung(req_payload, user_exist) 
    return latest_saldo

async def post_tarik(req_payload: RequestTarik) -> ResponseTarik:
    async with database.transaction():
        user_exist = await check_exist_by_no_rekening(req_payload.no_rekening)
        if not user_exist:
            remark = "Nomor Rekening Tidak Diketahui"
            logger.error(remark) 
            raise Exception(remark)
        latest_saldo = await create_tarik(req_payload, user_exist) 
    return latest_saldo

async def get_saldo(no_rekening: str) -> ResponseSaldo:
    async with database.transaction():
        user_exist = await check_exist_by_no_rekening(no_rekening)
        if not user_exist:
            remark = "Nomor Rekening Tidak Diketahui"
            logger.error(remark) 
            raise Exception(remark)
        latest_saldo = await read_latest_saldo(no_rekening)
    return latest_saldo

async def get_mutasi(no_rekening: str) -> ResponseMutasi:
    async with database.transaction():
        user_exist = await check_exist_by_no_rekening(no_rekening)
        if not user_exist:
            remark = "Nomor Rekening Tidak Diketahui"
            logger.error(remark) 
            raise Exception(remark)
        latest_saldo = await read_mutasi(no_rekening)
    return latest_saldo

