from fastapi import APIRouter, Body, HTTPException, Request, status

from src.controllers.account import Account
from src.controllers.authentication_operations import AuthenticationOperations
from src.controllers.customer import Customer

from src.helpers.custom_response import (
    error_response,
    valid_data_response,
    valid_response,
)
from src.helpers.rbac_decorator import role_based_access
from src.helpers.extract_jwt import extract_jwt_token
from src.helpers.validation_decorator import validate

from src.schemas.new_registration_schema import new_registration_schema
from src.schemas.update_customer_schema import update_customer_schema

from src.helpers.logger_config import CustomLogger

logger = CustomLogger(__name__)

router = APIRouter(prefix="", tags=["customer"])


@router.get("/customer/{account_no}")
@role_based_access(["Cashier", "Manager"])
def get_customer_details(request: Request, account_no):
    """get details of a customer

    Args:
        request (Request): Fast API request object
        account_no (int): account number of customer

    Returns:
        dict: A JSON response
    """
    logger.debug("Entering get_customer_details function")

    instance = Account()
    valid_account_details = instance.verify_account(account_no)
    logger.info("Verifying Account details")

    if valid_account_details is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account Not Found.")

    logger.info("Account details verified successfully.")

    user_id = valid_account_details[0]
    customer = Customer()
    user_details = customer.view_customer_details(user_id)

    logger.debug(f"user details : {user_details}")
    logger.info("Customer details retrieved successfully and returning valid response")

    return valid_data_response(200, user_details)


@router.post("/customer")
@validate(new_registration_schema)
@role_based_access(["Cashier", "Manager"])
def create_new_customer_account(request: Request, body_data=Body()):
    """create new customer account

    Args:
        request (Request): Fast API request object
        body_data (dict): data containing the customer details

    Returns:
        dict: A JSON response
    """
    logger.debug("Entering create_new_customer_account function")

    user_details = extract_jwt_token(request)
    role = user_details["role"]
    logger.debug(f"{role} : role retrieved from token successfully")

    username = body_data["username"]
    password = body_data["password"]
    name = body_data["name"]
    email = body_data["email"]
    phone = body_data["phone"]
    id_proof_type = body_data["id_proof_type"]
    id_proof = body_data["id_proof"]
    gender = body_data["gender"]

    instance = AuthenticationOperations(username, password)
    logger.info("Authentication instance created successfully.")

    customer_id = instance.create_customer_auth()
    if customer_id == -1:
        logger.warning(f"${username} Username already exists.")
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            error_response(400, "Username already exists."),
        )
    logger.debug(
        f"Customer Auth account created successfully with customer id : {customer_id}"
    )

    new_customer_details = (name, email, phone, id_proof_type, id_proof, gender)
    instance = Customer("Customer", *new_customer_details)
    message = instance.register_new_customer(customer_id, role)

    logger.info("Customer account created successfully")

    return valid_response(200, message)


@router.put("/customer")
@validate(update_customer_schema)
@role_based_access(["Cashier", "Manager"])
def update_customer_details(request: Request, body_data=Body()):
    """update customer details

    Args:
        request (Request): Fast API request object
        body_data (dict): data containing attribute to update

    Returns:
        dict: A JSON response
    """
    logger.debug("Entering update_customer_details function")

    user_details = extract_jwt_token(request)
    role = user_details["role"]
    logger.debug(f"{role}: role retrieved from token successfully")

    account_no = body_data["account_no"]
    attribute_to_update = body_data["attribute_to_update"]
    attribute_value = body_data["attribute_value"]

    instance = Account()
    valid_account = instance.verify_account(account_no)
    logger.debug("Account verified successfully")

    if not valid_account:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, error_response(404, "Account Not Found.")
        )

    user_id = valid_account[0]
    customer = Customer()
    message = customer.edit_customer_details(
        user_id, attribute_to_update, attribute_value, role
    )
    logger.info("Customer details updated successfully")
    return valid_response(200, message)
