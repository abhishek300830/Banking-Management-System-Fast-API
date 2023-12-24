import datetime
from unittest import TestCase
from unittest import mock

from src.controllers.authentication_operations import AuthenticationOperations


class TestAuthenticationOperations(TestCase):
    def setUp(self):
        self.instance = AuthenticationOperations()

    @mock.patch("src.controllers.authentication_operations.get_item")
    def test_valid_login(self, mock_get_item):
        mock_get_item.return_value = (
            5,
            "Gaurav123",
            "96a3dfa0b4ba697d379a1e6522979652306745eaa8a7e6eca890e3bcf6c6da51",
            "Customer",
            datetime.datetime(2023, 8, 27, 0, 33, 9),
            datetime.datetime(2023, 8, 27, 0, 33, 9),
        )

        valid_user_data = (
            5,
            "Gaurav123",
            "96a3dfa0b4ba697d379a1e6522979652306745eaa8a7e6eca890e3bcf6c6da51",
            "Customer",
            datetime.datetime(2023, 8, 27, 0, 33, 9),
            datetime.datetime(2023, 8, 27, 0, 33, 9),
        )

        self.instance.username = "Gaurav123"
        self.instance.password = "Gaurav123@"

        result = self.instance.login()
        self.assertEqual(result, valid_user_data)

    @mock.patch("src.controllers.authentication_operations.get_item")
    def test_invalid_username(self, mock_get_item):
        mock_get_item.return_value = None

        self.instance.username = "Gaurav12345"
        self.instance.password = "some_password"

        result = self.instance.login()
        self.assertIsNone(result)

    @mock.patch("src.controllers.authentication_operations.get_item")
    def test_invalid_password(self, mock_get_item):
        mock_get_item.return_value = (
            5,
            "Gaurav123",
            "96a3dfa0b4ba697d379a1e6522979652306745eaa8a7e6eca890e3bcf6c6da51",
            "Customer",
            datetime.datetime(2023, 8, 27, 0, 33, 9),
            datetime.datetime(2023, 8, 27, 0, 33, 9),
        )

        self.instance.username = "Gaurav123"
        self.instance.password = "wrong_password"

        result = self.instance.login()
        self.assertIsNone(result)

    @mock.patch("src.controllers.authentication_operations.update_item")
    @mock.patch("src.controllers.authentication_operations.get_item")
    def test_change_password_correct_old_pass(self, mock_get_item, mock_update_item):
        mock_update_item.return_value = None
        mock_get_item.return_value = (
            6,
            "Tushar123",
            "46dd6b68996dd1d1974f51650734b94c906f50e3d6ec0ff6ca98a23444812ce3",
            "Customer",
            datetime.datetime(2023, 8, 28, 0, 4, 55),
            datetime.datetime(2023, 8, 28, 0, 4, 55),
        )

        user_id = 6
        old_password = "Tushar123@"
        new_password = "qwerty1234@"
        result = self.instance.change_password(user_id, old_password, new_password)
        expected_result = {
            "code": 200,
            "details": "Password Updated Successfully.",
            "status": "success",
        }
        self.assertEqual(result, expected_result)

    @mock.patch("src.controllers.authentication_operations.update_item")
    @mock.patch("src.controllers.authentication_operations.get_item")
    def test_change_password_wrong_old_pass(self, mock_get_item, mock_update_item):
        mock_update_item.return_value = None
        mock_get_item.return_value = (
            6,
            "Tushar123",
            "46dd6b68996dd1d1974f51650734b94c906f50e3d6ec0ff6ca98a23444812ce3",
            "Customer",
            datetime.datetime(2023, 8, 28, 0, 4, 55),
            datetime.datetime(2023, 8, 28, 0, 4, 55),
        )

        user_id = 6
        old_password = "dadsffshar123@"
        new_password = "qwerty1234@"

        result = self.instance.change_password(user_id, old_password, new_password)
        espected_result = "Entered Old Password is Wrong."
        self.assertEqual(result, espected_result)

    @mock.patch("src.controllers.authentication_operations.get_item")
    @mock.patch("src.controllers.authentication_operations.insert_item")
    def test_create_customer_auth(self, mock_insert_item, mock_get_item):
        mock_insert_item.return_value = None
        mock_get_item.return_value = (
            11,
            "umani",
            "96e646358d68288ea5efc502ee850e256f111b67e1172b117312b56320ef3ced",
            "Customer",
        )
        self.instance.password = "qwerty123@"
        expected_user_id = 11
        user_id = self.instance.create_customer_auth()
        self.assertEqual(user_id, expected_user_id)
