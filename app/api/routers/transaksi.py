from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import core.repositories.transaksi as transaksi_repo
import core.schemas.transaksi as transaksi_schema 

from api.routers.log import logger

router = APIRouter()

@router.post('/tabung', tags=["Transaksi"], status_code=status.HTTP_200_OK)
async def create_tabung(create_tabung_payload: transaksi_schema.RequestTabung):
    try:
        data_creation_success = await transaksi_repo.create_tabung(create_tabung_payload)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code=400,
            content={"remark": str(e)},
        )

@router.post('/tarik', tags=["Transaksi"], status_code=status.HTTP_200_OK)
async def create_tarik(create_tarik_payload: transaksi_schema.RequestTarik):
    try:
        data_creation_success = await transaksi_repo.create_tarik(create_tarik_payload)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code=400,
            content={"remark": str(e)},
        )

@router.get('/saldo/{no_rekening}', tags=["Transaksi"], status_code=status.HTTP_200_OK)
async def get_saldo(no_rekening: str):
    try:
        data_creation_success = await transaksi_repo.get_saldo(no_rekening)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code=400,
            content={"remark": str(e)},
        )

@router.get('/mutasi/{no_rekening}', tags=["Transaksi"], status_code=status.HTTP_200_OK)
async def get_mutasi(no_rekening: str):
    try:
        data_creation_success = await transaksi_repo.get_mutasi(no_rekening)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code=400,
            content={"remark": str(e)},
        )
