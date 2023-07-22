from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from api.schemas.user_management import RequestDaftar, ResponseDaftar
from services.user_management import post_user
from api.routers.log import logger


router = APIRouter()

@router.post('/daftar', tags=["User Management"], status_code=status.HTTP_200_OK, response_model=ResponseDaftar)
async def create_user(create_user_payload: RequestDaftar) -> ResponseDaftar:
    try:
        data_creation_success = await post_user(create_user_payload)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code=400,
            content={"remark": str(e)},
        )