from src.helpers.logger_config import CustomLogger
from src.helpers.runtime_queries import QUERIES
from src.models.database import get_items, update_item, get_item

logger = CustomLogger(__name__)


class RequestsHandler:
    """Handler for requests"""

    def __init__(self):
        self.withdrawn_requests = None
        self.new_registration_requests = None
        self.modification_requests = None
        self.total_no_of_requests = None

    def find_total_no_of_requests(self):
        """find total number of requests

        Returns:
            int: total number of requests
        """
        logger.info("Finding total number of requests")

        self.withdrawn_requests = get_items(
            QUERIES.get("SEARCH_IN_ACCOUNT_WITHDRAWN_REQUESTS"), ("Pending",)
        )
        self.new_registration_requests = get_items(
            QUERIES.get("SEARCH_USERS_BY_ACCOUNT_STATUS"), (0,)
        )
        self.modification_requests = get_items(
            QUERIES.get("SEARCH_PENDING_REQ_IN_DETAIL_MODIFICATION"), ("Pending",)
        )

        self.total_no_of_requests = (
            len(self.withdrawn_requests)
            + len(self.new_registration_requests)
            + len(self.modification_requests)
        )
        logger.info(f"Total number of requests: {self.total_no_of_requests}")
        return self.total_no_of_requests

    def check_for_withdraw_requests(self):
        """checks for withdraw requests pending

        Returns:
            list: list of requests pending
        """
        logger.info("Checking for withdraw requests")
        return self.withdrawn_requests

    def approve_withdrawn_request(self, user_id, amount, done_by, request_id, comment):
        """approval pending withdrawn requests

        Args:
            user_id (int): user id of customer
            amount (int):  amount to be approved
            done_by (string):  done by which Cashier or Manager
            request_id (int): request id of request
            comment (string): any comment
        """
        logger.info(f"Approving withdrawn request for user_id: {user_id}")
        user_account_details = get_item(
            QUERIES.get("SEARCH_IN_USER_ACCOUNT_BY_ID"), (user_id,)
        )
        account_number = user_account_details[1]
        current_balance = user_account_details[3]
        pending_amount = user_account_details[4]
        pending_amount = str(int(pending_amount) + int(amount))
        final_balance = str(current_balance - float(amount))

        update_item(
            QUERIES.get("UPDATE_AMOUNT_IN_ACCOUNT"), (final_balance, account_number)
        )
        update_item(
            QUERIES.get("UPDATE_TRANSACTION_OF_ACCOUNT"),
            (account_number, "Debit", amount, done_by),
        )
        update_item(
            QUERIES.get("UPDATE_PENDING_AMOUNT_IN_ACCOUNT"), (pending_amount, user_id)
        )

        update_item(
            QUERIES.get("UPDATE_IN_ACCOUNT_WITHDRAWN_REQUESTS"),
            ("Approved", "Manager", comment, request_id),
        )
        logger.info(f"Withdrawn request approved for user_id: {user_id}")

    def reject_withdrawn_request(self, user_id, amount, request_id, comment):
        """reject a pending withdraw request

        Args:
            user_id (int): user id of customer
            amount (int):  amount to be approved
            request_id (int): request id of request
            comment (string): any comment
        """
        logger.info(f"Rejecting withdrawn request for user_id: {user_id}")
        user_account_details = get_item(
            QUERIES.get("SEARCH_IN_USER_ACCOUNT_BY_ID"), (user_id,)
        )

        pending_amount = user_account_details[4]
        pending_amount = str(int(pending_amount) + int(amount))
        update_item(
            QUERIES.get("UPDATE_PENDING_AMOUNT_IN_ACCOUNT"), (pending_amount, user_id)
        )

        update_item(
            QUERIES.get("UPDATE_IN_ACCOUNT_WITHDRAWN_REQUESTS"),
            ("Rejected", "Manager", comment, request_id),
        )
        logger.info(f"Withdrawn request rejected for user_id: {user_id}")

    def check_for_new_registration_request(self):
        """check if new registration request

        Returns:
            list: list of registration requests
        """
        logger.info("Checking for new registration requests")
        return self.new_registration_requests

    def approve_or_reject_registeration_request(self, user_id, manager_choice):
        """approve or reject registration request

        Args:
            user_id (int):  ID of the user
            manager_choice (string): approved or rejected
        """
        logger.info(
            f"Approving or rejecting registration request for user_id: {user_id}"
        )
        if manager_choice == "approved":
            update_item(
                QUERIES.get("UPDATE_VERIFIED_STATUS_OF_CUSTOMER"),
                (
                    "1",
                    user_id,
                ),
            )
        elif manager_choice == "rejected":
            update_item(
                QUERIES.get("UPDATE_VERIFIED_STATUS_OF_CUSTOMER"),
                (
                    "2",
                    user_id,
                ),
            )
        logger.info(f"Registration request for user_id: {user_id} {manager_choice}")

    def check_for_user_modification_request(self):
        """check for user modification requests

        Returns:
            list:  List of  user modification requests
        """
        logger.info("Checking for user modification requests")
        return self.modification_requests

    def approve_or_reject_modification_requests(
        self, attribute_to_update, attribute_value, user_id, request_id, manager_choice
    ):
        """approve or reject modification request

        Args:
            attribute_to_update (string): attribute of update name,email,phone,gender
            attribute_value (string): attribute value of selected
            user_id (int): user id of customer
            request_id (int): request id of customer
            manager_choice (string): status approved or rejected
        """
        logger.info(
            f"Approving or rejecting modification request for user_id: {user_id}"
        )
        if manager_choice == "approved":
            update_item(
                QUERIES.get("UPDATE_USERS_BY_ID").format(attribute_to_update),
                (attribute_value, user_id),
            )
            update_item(
                QUERIES.get("UPDATE_USER_DETAIL_MODIFICATION_STATUS"),
                ("Approved", request_id),
            )
        elif manager_choice == "rejected":
            update_item(
                QUERIES.get("UPDATE_USER_DETAIL_MODIFICATION_STATUS"),
                ("Rejected", request_id),
            )
        logger.info(f"Modification request for user_id: {user_id} {manager_choice}")
