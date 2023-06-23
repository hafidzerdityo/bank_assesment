from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DATE, Table, DateTime, Numeric
from sqlalchemy.orm import relationship
from db.database_config import metadata, SQLALCHEMY_DATABASE_URL


Nasabah = Table(
    "nasabah",
    metadata,
    Column('no_rekening',String(255), primary_key=True, index=True, nullable=False),
    Column('no_hp',String(20), unique=True, index=True, nullable=False),
    Column('nik',String(255), unique=True, index=True, nullable=False),
    Column('nama',String(255), index=True, nullable=False),
    Column('saldo', Numeric(precision=10, scale=2), index=True, nullable=False),
)

Transaksi = Table(
    'transaksi',
    metadata, 
    Column('id',Integer, primary_key=True, index=True),
    Column('kode_transaksi' ,String(1), index=True),
    Column('waktu' ,DateTime, index=True, nullable=False),
    Column('nominal', Numeric(precision=10, scale=2), index=True, nullable=False),
    Column('no_rekening',String(255), ForeignKey("nasabah.no_rekening"), index=True, nullable=False)
)
