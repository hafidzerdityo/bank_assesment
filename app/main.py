from fastapi import FastAPI,Request, APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, StrictStr
import uvicorn
import json
import pandas as pd
import re
import os
from datetime import date

from db.database_config import metadata, engine, database
import api.routers.user_management as user_management_router
import api.routers.transaksi as transaksi_router

app = FastAPI(title="API Bank Assesment",
    description="author: Muhammad Hafidz Erdityo",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user_management_router.router)
app.include_router(transaksi_router.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8004, workers=2)
