from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import core.repositories.user_management as user_management_repo
import core.schemas.user_management as user_management_schema 
from api.routers.log import logger

router = APIRouter()

@router.post('/daftar', tags=["User Management"], status_code=status.HTTP_200_OK)
async def create_user(create_user_payload: user_management_schema.RequestDaftar):
    try:
        data_creation_success = await user_management_repo.create_user(create_user_payload)
        return data_creation_success 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
                status_code=400,
                content={"remark": str(e)},
            )