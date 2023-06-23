# import asyncio
# from unittest import TestCase
# from unittest.mock import patch
# from datetime import datetime

# import core.repositories.user_management as user_management_repo
# import core.repositories.transaksi as transaksi_repo
# import core.schemas.user_management as user_management_schema
# import core.schemas.transaksi as transaksi_schema


# class CreateUserTest(TestCase):
#     @patch('core.repositories.utils.generate_unique_account_number')
#     @patch('db.database_config.database')
#     def test_create_user(self, mock_database, mock_generate_account_number):
#         mock_database.fetch_one.return_value = None
#         mock_generate_account_number.return_value = '1234567890'
#         payload = user_management_schema.RequestDaftar(
#             no_hp='08123456789',
#             nama='Erick Thohir',
#             nik='119900',
#         )
#         result = asyncio.run(user_management_repo.create_user(payload))
#         self.assertEqual(len(result.no_rekening), 10)
#         self.assertTrue(result.no_rekening.isdigit())
