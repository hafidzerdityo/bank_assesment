from api.schemas.user_management import RequestDaftar, ResponseDaftar
from adapters.postgres.user_management import check_user, create_user, database

async def post_user(req_payload: RequestDaftar) -> ResponseDaftar:
    async with database.transaction():
        user_exist = await check_user(req_payload.no_hp, req_payload.nik)
        if user_exist:
            raise Exception("Nomor HP atau NIK Sudah Terdaftar")

        get_rekening = await create_user(req_payload=req_payload)

    return get_rekening


