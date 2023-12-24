from datetime import datetime
from unittest import TestCase
from unittest import mock

from src.controllers.customer import Customer


class TestCustomer(TestCase):
    def setUp(self) -> None:
        self.instance = Customer()

    @mock.patch("src.controllers.customer.insert_item")
    def test_register_new_customer_by_manager(self, mock_insert_item):
        mock_insert_item.return_value = None

        result = self.instance.register_new_customer(6, "Manager")
        expected_result = "Account Created Successfully"
        self.assertEqual(result, expected_result)

    @mock.patch("src.controllers.customer.insert_item")
    def test_register_new_customer_by_cashier(self, mock_insert_item):
        mock_insert_item.return_value = None

        result = self.instance.register_new_customer(6, "Cashier")
        expect_result = "Account Approval Request sent to Manager"
        self.assertEqual(result, expect_result)

    @mock.patch("src.controllers.customer.insert_item")
    def test_create_customer_account(self, mock_insert_item):
        mock_insert_item.return_value = None
        result = self.instance.create_customer_account(6)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.customer.insert_item")
    def test_edit_customer_details_by_cashier(self, mock_insert_item):
        mock_insert_item.return_value = None

        result = self.instance.edit_customer_details(6, "name", "naugs", "Cashier")
        expected_result = "Details Updation Request sent Successfully."
        self.assertEqual(result, expected_result)

    @mock.patch("src.controllers.customer.update_item")
    def test_edit_customer_details_by_manager(self, mock_update_item):
        mock_update_item.return_value = None
        result = self.instance.edit_customer_details(6, "name", "naugs", "Manager")

        expected_result = "Details Updated Successfully."
        self.assertEqual(result, expected_result)

    @mock.patch("src.controllers.customer.get_item")
    def test_view_customer_details(self, mock_get_item):
        mock_get_item.return_value = (
            6,
            "Tushar",
            "Tushar@gmail.com",
            "2136548970",
            "Aadhar Card",
            "987654321",
            "Male",
            1,
            datetime(2023, 8, 28, 0, 5, 25),
            datetime(2023, 8, 28, 0, 5, 25),
        )

        result = self.instance.view_customer_details(6)
        expected = {
            "Name": "Tushar",
            "Email": "Tushar@gmail.com",
            "Phone": "2136548970",
            "ID Type": "Aadhar Card",
            "ID Number": "987654321",
            "Gender": "Male",
        }
        self.assertEqual(result, expected)
