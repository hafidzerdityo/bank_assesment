from datetime import datetime
import hashlib
import random
import core.models.db_model as db_model
from db.database_config import database


def get_current_datetime():
    return datetime.now()

def hash_with_sha_256(text):
    return hashlib.sha256(text.encode()).hexdigest()

async def generate_unique_account_number() -> str:
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    while True:
        account_number = ''.join(random.choices(digits, k=10))
        check_no_rek = db_model.Nasabah.select().where(db_model.Nasabah.c.no_rekening == account_number)
        check_no_rek = await database.fetch_one(check_no_rek)
        if not check_no_rek:
            return account_number
