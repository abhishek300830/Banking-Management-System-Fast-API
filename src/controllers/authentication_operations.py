import hashlib
from src.helpers.logger_config import CustomLogger

from src.helpers.custom_response import valid_response

from src.helpers.runtime_queries import QUERIES
from src.models.database import get_item, insert_item, update_item

logger = CustomLogger(__name__)


class AuthenticationOperations:
    """This class provides all the functionality to all authentication operations"""

    username = any
    password = any
    role = any

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def login(self):
        """Authenticate user credentials to the database

        Returns:
            (Dict,None): if user is authenticated returns users otherwise returns None
        """
        logger.info(f"Attempting to login with username: {self.username}")
        valid_user = get_item(QUERIES.get("SEARCH_USER_BY_USERNAME"), (self.username,))

        if valid_user is None:
            logger.warning(f"Invalid username: {self.username}")
            return None, None

        hashed_password = self.__hashing_password()
        valid_password = valid_user[2]

        if hashed_password == valid_password:
            self.__assigning_role(valid_user[3])
            logger.info(f"User logged in successfully: {self.username}")
            userDetails = get_item(QUERIES.get("SEARCH_USER_BY_ID"), (valid_user[0],))
            return valid_user, userDetails

        logger.warning(f"Invalid password for username: {self.username}")
        return None, None

    def change_password(self, user_id, old_password, new_password):
        """Change user password

        Args:
            user_id (int): user id of logged in user
            old_password (string): old password of user
            new_password (string): new password of user

        Returns:
            dict: valid JSON object
        """
        self.password = old_password
        hashed_old_password = self.__hashing_password()

        valid_user_details = get_item(QUERIES.get("SEARCH_AUTH_BY_ID"), (user_id,))
        valid_password = valid_user_details[2]

        if valid_password == hashed_old_password:
            self.password = new_password
            hashed_new_password = self.__hashing_password()

            update_item(
                QUERIES.get("UPDATE_PASSWORD_IN_AUTH"),
                (hashed_new_password, user_id),
            )
            logger.info(f"Password changed successfully for user id: {user_id}")
            return True

        logger.warning(f"Invalid old password for user id: {user_id}")
        return False

    def __hashing_password(self):
        """generate hash for password

        Returns:
            String: hash of the password
        """
        encoded_password = self.password.encode()
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        return hashed_password

    def __assigning_role(self, user_role):
        """assign role to self.role

        Args:
            user_role (string): user role to assign
        """
        self.role = user_role

    def create_customer_auth(self):
        """create customer auth for validation

        Returns:
            String: returns user id
        """
        hashed_password = self.__hashing_password()
        logger.info("Checking new customer Details already exists or not")
        user_found = get_item(QUERIES.get("SEARCH_USER_BY_USERNAME"), (self.username,))

        if user_found:
            logger.debug(f"${self.username} already exists")
            logger.error("Username already exists")
            return -1

        insert_item(
            QUERIES.get("INSERT_INTO_AUTH_TABLE"),
            (self.username, hashed_password, "Customer"),
        )
        logger.info("customer auth created successfully")
        user_auth = get_item(QUERIES.get("SEARCH_USER_BY_USERNAME"), (self.username,))
        logger.info(f"Customer auth created for username: {self.username}")
        return user_auth[0]
