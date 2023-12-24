from src.helpers.logger_config import CustomLogger
from src.controllers.user import User
from src.helpers.runtime_queries import QUERIES
from src.models.database import get_item, insert_item, update_item

logger = CustomLogger(__name__)


class Customer(User):
    """This class represents a customer and provides access to operations performed on customer"""

    def register_new_customer(self, user_id, user_role):
        """Register a new customer

        Args:
            user_id (int): user id of customer to register
            user_role (string): role of account creator

        Returns:
            String: message about account status
        """
        logger.info("Registering a new customer")
        if user_role == "Manager":
            verified = 1
        else:
            verified = 0
        customer_details = (
            user_id,
            self.name,
            self.email,
            self.phone_no,
            self.id_proof_type,
            self.id_proof,
            self.gender,
            verified,
        )
        insert_item(QUERIES.get("INSERT_INTO_USERS_TABLE"), customer_details)

        self.create_customer_account(user_id)

        if user_role == "Manager":
            logger.info("Account Created Successfully")
            return "Account Created Successfully"

        logger.info("Account Approval Request sent to Manager")
        return "Account Approval Request sent to Manager"

    def create_customer_account(self, user_id):
        """create customer account

        Args:
            user_id (int): user id of customer
        """
        logger.info("Creating customer account")
        account_number = str(int(user_id) * 1000)
        account_type = "Saving"
        account_balance = 2500
        pending_balance = 0
        account_details = (
            user_id,
            account_number,
            account_type,
            account_balance,
            pending_balance,
        )
        insert_item(QUERIES.get("INSERT_INTO_ACCOUNT_TABLE"), account_details)

    def edit_customer_details(
        self, user_id, attribute_to_update, attribute_value, role
    ):
        """Modify customer details

        Args:
            user_id (int):  user id of customer
            attribute_to_update (string):  any attribute to update out of name,email,phone,gender
            attribute_value (string): value of attribute chosen by user
            role (string): role of logged in user

        Returns:
            String: message about status of modifications
        """
        logger.info("Modifying customer details")
        if role == "Manager":
            update_item(
                QUERIES.get("UPDATE_USERS_BY_ID").format(attribute_to_update),
                (attribute_value, user_id),
            )
            logger.info("Details Updated Successfully.")
            return "Details Updated Successfully."

        insert_item(
            QUERIES.get("INSERT_INTO_USER_DETAIL_MODIFICATION"),
            (user_id, attribute_to_update, attribute_value, "Pending"),
        )
        logger.info("Details Updation Request sent Successfully.")
        return "Details Updation Request sent Successfully."

    def view_customer_details(self, user_id):
        """view_customer_details used by cashier and manager

        Args:
            user_id (int): user id of the customer

        Returns:
            dict: a dictionary containing customer details
        """
        logger.info("Viewing customer details")
        user_details = get_item(QUERIES.get("SEARCH_USER_BY_ID"), (user_id,))

        user_details_list = {
            "Name": user_details[1],
            "Email": user_details[2],
            "Phone": user_details[3],
            "ID Type": user_details[4],
            "ID Number": user_details[5],
            "Gender": user_details[6],
        }

        return user_details_list
