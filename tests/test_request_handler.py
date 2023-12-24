import datetime
from unittest import TestCase
from unittest import mock

from src.controllers.request_handler import RequestsHandler


class TestRequestAccount(TestCase):

    def setUp(self):
        self.instance = RequestsHandler()

    @mock.patch("src.controllers.request_handler.get_items")
    def test_find_total_no_of_requests(self, mock_get_items):
        mock_get_items.return_value = []

        result = self.instance.find_total_no_of_requests()
        self.assertEqual(result, 0)

    def test_check_for_withdraw_requests(self):
        requests = self.instance.check_for_withdraw_requests()
        self.assertIsNone(requests)

    @mock.patch("src.controllers.request_handler.update_item")
    @mock.patch("src.controllers.request_handler.get_item")
    def test_approve_withdrawn_request(self, mock_get_item, mock_update_item):
        mock_get_item.return_value = (6, '6000', 'Saving', 100109.0, -12000.0, datetime.datetime(2023, 8, 28, 0, 5, 25),
                                      datetime.datetime(2023, 8, 28, 0, 5, 25))
        mock_update_item.return_value = None
        user_id = 6
        amount = 12000
        done_by = "Cashier"
        request_id = 1
        comment = "okay"

        result = self.instance.approve_withdrawn_request(user_id, amount, done_by, request_id, comment)
        self.assertEqual(result, None)

    @mock.patch("src.controllers.request_handler.update_item")
    @mock.patch("src.controllers.request_handler.get_item")
    def test_reject_withdrawn_request(self, mock_get_item, mock_update_item):
        mock_get_item.return_value = (6, '6000', 'Saving', 100109.0, -12000.0, datetime.datetime(2023, 8, 28, 0, 5, 25),
                                      datetime.datetime(2023, 8, 28, 0, 5, 25))
        mock_update_item.return_value = None
        user_id = 6
        amount = 12000
        request_id = 1
        comment = "okay"
        result = self.instance.reject_withdrawn_request(user_id, amount, request_id, comment)
        self.assertIsNone(result)

    def test_check_for_new_registration_request(self):
        result = self.instance.check_for_new_registration_request()
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_registeration_request_choice_1(self, mock_update_item):
        mock_update_item.return_value = None
        user_id = 6
        manager_choice = 1
        result = self.instance.approve_or_reject_registeration_request(user_id, manager_choice)
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_registeration_request_choice_2(self, mock_update_item):
        mock_update_item.return_value = None
        user_id = 6
        manager_choice = 2
        result = self.instance.approve_or_reject_registeration_request(user_id, manager_choice)
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_registeration_request_choice_3(self, mock_update_item):
        mock_update_item.return_value = None
        user_id = 6
        manager_choice = 3
        result = self.instance.approve_or_reject_registeration_request(user_id, manager_choice)
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_registeration_request_choice_4(self, mock_update_item):
        mock_update_item.return_value = None
        user_id = 6
        manager_choice = 4
        result = self.instance.approve_or_reject_registeration_request(user_id, manager_choice)
        self.assertIsNone(result)

    def test_check_for_user_modification_request(self):
        result = self.instance.check_for_user_modification_request()
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_modification_requests_choice_1(self,mock_update_item):
        mock_update_item.return_value = None
        attribute_to_update = "name"
        attribute_value = "Abhishek"
        user_id = 1
        request_id = 1
        manager_choice = 1

        result = self.instance.approve_or_reject_modification_requests(attribute_to_update, attribute_value, user_id, request_id,
                                                manager_choice)
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_modification_requests_choice_2(self, mock_update_item):
        mock_update_item.return_value = None
        attribute_to_update = "name"
        attribute_value = "Abhishek"
        user_id = 1
        request_id = 1
        manager_choice = 2

        result = self.instance.approve_or_reject_modification_requests(attribute_to_update, attribute_value, user_id, request_id,
                                                              manager_choice)
        self.assertIsNone(result)

    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_modification_requests_choice_3(self, mock_update_item):
        mock_update_item.return_value = None
        attribute_to_update = "name"
        attribute_value = "Abhishek"
        user_id = 1
        request_id = 1
        manager_choice = 3

        result = self.instance.approve_or_reject_modification_requests(attribute_to_update, attribute_value, user_id, request_id,
                                                              manager_choice)
        self.assertIsNone(result)


    @mock.patch("src.controllers.request_handler.update_item")
    def test_approve_or_reject_modification_requests_choice_4(self, mock_update_item):
        mock_update_item.return_value = None
        attribute_to_update = "name"
        attribute_value = "Abhishek"
        user_id = 1
        request_id = 1
        manager_choice = 4

        result = self.instance.approve_or_reject_modification_requests(attribute_to_update, attribute_value, user_id, request_id,
                                                              manager_choice)
        self.assertIsNone(result)
