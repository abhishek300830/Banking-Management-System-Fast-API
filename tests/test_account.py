import datetime
from unittest import TestCase
from unittest import mock

from src.controllers.account import Account


class TestAccount(TestCase):
    def setUp(self):
        self.instance = Account()

    @mock.patch("src.controllers.account.update_item")
    def test_deposit_amount(self, mock_update_item):
        mock_update_item.return_value = None
        amount = "100"
        done_by = "Manager"
        self.instance.account_balance = 10000
        result = self.instance.deposit_amount(amount, done_by)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.account.update_item")
    def test_withdraw_amount_done_by_manager(self, mock_update_item):
        mock_update_item.return_value = None
        amount = "100"
        done_by = "Manager"
        self.instance.account_balance = 10000
        result = self.instance.withdraw_amount(amount, done_by)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.account.update_item")
    def test_withdraw_amount_done_by_cashier(self, mock_update_item):
        mock_update_item.return_value = None
        amount = "100"
        done_by = "Cashier"
        self.instance.account_balance = 10000
        result = self.instance.withdraw_amount(amount, done_by)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.account.insert_item")
    @mock.patch("src.controllers.account.get_item")
    @mock.patch("src.controllers.account.update_item")
    def test_withdraw_amount_done_by_cashier_amount_greater_than_10000(
        self, mock_update_item, mock_get_item, mock_insert_item
    ):
        mock_get_item.return_value = (1,)
        mock_update_item.return_value = None
        mock_insert_item.return_value = None
        amount = "12000"
        done_by = "Cashier"
        self.instance.account_balance = 15000
        self.instance.pending_balance = 0
        result = self.instance.withdraw_amount(amount, done_by)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.account.get_item")
    def test_view_balance(self, mock_get_item):
        mock_get_item.return_value = (
            5,
            "5000",
            "Saving",
            14848.0,
            0.0,
            datetime.datetime(2023, 8, 27, 0, 33, 44),
            datetime.datetime(2023, 8, 27, 0, 33, 44),
        )

        user_valid_details = (
            5,
            "5000",
            "Saving",
            14848.0,
            0.0,
            datetime.datetime(2023, 8, 27, 0, 33, 44),
            datetime.datetime(2023, 8, 27, 0, 33, 44),
        )

        result = self.instance.view_balance(5)

        self.assertEqual(result, user_valid_details)

    @mock.patch("src.controllers.account.get_item")
    def test_set_customer_account_details(self, mock_get_item):
        mock_get_item.return_value = (
            5,
            "5000",
            "Saving",
            14848.0,
            0.0,
            datetime.datetime(2023, 8, 27, 0, 33, 44),
            datetime.datetime(2023, 8, 27, 0, 33, 44),
        )

        result = self.instance.set_customer_account_details(6)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.account.get_items")
    @mock.patch("src.controllers.account.get_item")
    def test_print_passbook(self, mock_get_item, mock_get_items):
        mock_get_item.return_value = (
            5,
            "5000",
            "Saving",
            14848.0,
            0.0,
            datetime.datetime(2023, 8, 27, 0, 33, 44),
            datetime.datetime(2023, 8, 27, 0, 33, 44),
        )
        mock_get_items.return_value = [
            {
                "account_number": "6000",
                "transaction_type": "Credit",
                "amount": 500.0,
                "date_and_time": "2023-08-28T20:20:11",
                "done_by": "Customer",
            },
            {
                "account_number": "6000",
                "transaction_type": "Credit",
                "amount": 100.0,
                "date_and_time": "2023-08-29T14:52:23",
                "done_by": "Customer",
            },
        ]
        result = self.instance.print_passbook(5)
        expected_result = [
            {
                "account_number": "6000",
                "transaction_type": "Credit",
                "amount": 500.0,
                "date_and_time": "2023-08-28T20:20:11",
                "done_by": "Customer",
            },
            {
                "account_number": "6000",
                "transaction_type": "Credit",
                "amount": 100.0,
                "date_and_time": "2023-08-29T14:52:23",
                "done_by": "Customer",
            },
        ]
        self.assertEqual(result, expected_result)

    @mock.patch("src.controllers.account.get_item")
    def test_verify_account(self, mock_get_item):
        mock_get_item.return_value = (
            6,
            "6000",
            "Saving",
            112099.0,
            0.0,
            datetime.datetime(2023, 8, 28, 0, 5, 25),
            datetime.datetime(2023, 8, 28, 0, 5, 25),
        )

        result = self.instance.verify_account(6000)

        valid_response = (
            6,
            "6000",
            "Saving",
            112099.0,
            0.0,
            datetime.datetime(2023, 8, 28, 0, 5, 25),
            datetime.datetime(2023, 8, 28, 0, 5, 25),
        )

        self.assertEqual(result, valid_response)
