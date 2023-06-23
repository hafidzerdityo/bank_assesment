Untuk Run Service Gunakan "docker-compose up" pada root directory.

Semua port di bind dari port docker container 8004 ke port host 8004

1. Daftar

endpoint(POST): http://127.0.0.1:8004/daftar

contoh payload:
{
    "nama": "Winahyo",
    "nik": "12345638",
    "no_hp": "08211867478"
}

contoh response:
{
    "no_rekening": "7823427205" 
}

*Nik dan no_hp harus berupa string yang berisi digit(0-9).
Response berupa no_rekening bisa digunakan untuk semua endpoint dibawah.

2. Tabung

endpoint(POST): http://127.0.0.1:8004/tabung

contoh payload:
{
    "no_rekening": "7823427205",
    "nominal": 1000
}

contoh response:
{
    "saldo": 1000.0
}

*nominal dapat berupa integer ataupun float

3. Tarik

endpoint(POST): http://127.0.0.1:8004/tarik

contoh payload:
{
    "no_rekening": "7823427205",
    "nominal": 1000
}

contoh response:
{
    "saldo": 1000.0
}

4. /saldo/{no_rekening}

endpoint(GET): http://127.0.0.1:8004/saldo/{no_rekening}

contoh path parameter = http://127.0.0.1:8004/saldo/7823427205

contoh response:
{
    "saldo": 0.0
}

5. /mutasi/{no_rekening}

endpoint(GET): http://127.0.0.1:8004/mutasi/{no_rekening}

contoh path parameter = http://127.0.0.1:8004/mutasi/7823427205

contoh response:
[
    {
        "kode_transaksi": "C",
        "waktu": "2023-06-23 10:24:25",
        "nominal": 1000.0
    },
    {
        "kode_transaksi": "D",
        "waktu": "2023-06-23 10:27:46",
        "nominal": 1000.0
    }
]
