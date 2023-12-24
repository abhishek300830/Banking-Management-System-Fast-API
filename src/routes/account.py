from fastapi import APIRouter, Body, HTTPException, Request, status

from src.controllers.request_handler import RequestsHandler
from src.controllers.account import Account

from src.helpers.custom_response import error_response, valid_response
from src.helpers.rbac_decorator import role_based_access
from src.helpers.extract_jwt import extract_jwt_token
from src.helpers.validation_decorator import validate

from src.schemas.deposit_and_withdraw_schema import deposit_and_withdraw_schema
from src.schemas.all_requests_schema import all_requests_schema
from src.schemas.withdrawn_request_schema import withdrawn_request_schema
from src.schemas.registration_request_schema import registration_request_schema
from src.schemas.modification_request_schema import modification_request_schema
from src.schemas.transfer_funds_schema import transfer_funds_schema


from src.helpers.logger_config import CustomLogger

logger = CustomLogger(__name__)

router = APIRouter(prefix="", tags=["account"])


@router.put("/account/deposit")
@validate(deposit_and_withdraw_schema)
@role_based_access(["Cashier", "Manager"])
def deposit_amount(request: Request, body_data=Body()):
    """deposit amount to customer account

    Args:
        request (Request):
        body_data : account details to deposit

    Returns:
        dict: a json object
    """
    user_details = extract_jwt_token(request)
    role = user_details["role"]
    logger.debug(f"extracted role from json web token is {role}")

    instance = Account()
    account_number = body_data["account_number"]
    is_valid_account = instance.verify_account(account_number)

    if is_valid_account:
        logger.debug(f"Account number: {account_number} verified successfully")
        amount = body_data["amount"]
        instance.deposit_amount(amount, role)

        logger.info("account created successfully.")
        logger.debug(f"Amount Rs. {amount} credited to the account.")

        return valid_response(200, f"Rs. {amount} Credited Successfully.")

    logger.error("Customer Account not Found.")
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        error_response(404, "Customer Account not Found."),
    )


@router.put("/account/withdraw")
@validate(deposit_and_withdraw_schema)
@role_based_access(["Cashier", "Manager"])
def withdraw_amount(request: Request, body_data=Body()):
    """withdraw amount from a customer account

    Args:
        request (Request): fastAPI request object
        body_data (JSON, optional): request body data


    Returns:
        json: status of the API call
    """
    user_details = extract_jwt_token(request)
    role = user_details["role"]

    instance = Account()
    account_number = body_data["account_number"]
    is_valid_account = instance.verify_account(account_number)

    if is_valid_account:
        amount = body_data["amount"]
        current_balance = int(instance.account_balance) + int(instance.pending_balance)
        if int(amount) < int(current_balance):
            instance.withdraw_amount(amount, role)

            if role == "Cashier" and amount >= 10000:
                logger.info("Withdrawn Request Sent for Approval to Manager")
                return valid_response(
                    200, "Withdrawn Request Sent for Approval to Manager"
                )

            logger.info("amount debited successfully")
            return valid_response(200, f"Rs {amount} Debited Successfully.")

        logger.info("amount to withdraw is more than account balance")
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Amount to Withdraw is more than Account Balance",
        )

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer Account not Found.")


@router.get("/account/balance")
@role_based_access(["Customer"])
def get_account_balance(request: Request):
    """get account balance of customer

    Args:
        request (Request): The request

    Returns:
        dict: dict of account details
    """
    instance = Account()

    user_details = extract_jwt_token(request)
    user_id = user_details["user_id"]

    user_account_details = instance.view_balance(user_id)

    logger.info("account balance retrieved successfully")

    return {
        "account_number": user_account_details[1],
        "account_balance": user_account_details[3],
        "pending_balance": user_account_details[4],
    }


@router.get("/account/passbook")
@role_based_access(["Customer"])
def get_account_passbook(request: Request):
    """get account passbook of customer

    Args:
        request (Request): FastAPI request object

    Returns:
        list: list of account transactions
    """
    instance = Account()

    user_details = extract_jwt_token(request)
    user_id = user_details["user_id"]

    account_transactions = instance.print_passbook(user_id)
    if not account_transactions:
        logger.info("account transaction not found")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Account Transactions not Found."
        )

    my_transactions_data = []

    for transaction in account_transactions:
        response = {
            "account_number": transaction[1],
            "transaction_type": transaction[2],
            "amount": transaction[3],
            "date_and_time": transaction[4],
            "done_by": transaction[5],
        }

        my_transactions_data.append(response)

    logger.info("account transaction retrieved")

    return my_transactions_data


@router.put("/account/transfer_amount")
@validate(transfer_funds_schema)
@role_based_access(["Customer"])
def transfer_funds(request: Request, body_data=Body()):
    """Endpoint for transfer funds.

    Args:
        request (Request):  FastAPI request object
        body_data : account details to transfer

    Returns:
        dict: json response object
    """
    user_details = extract_jwt_token(request)
    user_id = user_details["user_id"]
    role = user_details["role"]

    amount_to_transfer = body_data["amount_to_transfer"]
    account_to_transfer = body_data["account_to_transfer"]

    instance = Account()
    instance.set_customer_account_details(user_id)
    logger.debug("customer details set to transfer")

    if float(amount_to_transfer) > float(instance.account_balance):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            error_response(400, "Make sure you have sufficient account Balance."),
        )
    else:
        account_details = instance.verify_account(account_to_transfer)
        if account_details is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                error_response(400, "Please Enter valid Account Number"),
            )

        else:
            instance.deposit_amount(amount_to_transfer, role)
            instance.set_customer_account_details(user_id)
            instance.withdraw_amount(amount_to_transfer, role)

            logger.info("Amount transferred successfully")

            return valid_response(200, "Amount Transfered Successfully.")


@router.get("/account/requests")
@role_based_access(["Manager", "Cashier"])
def get_pending_requests(request: Request):
    req_instance = RequestsHandler()
    total_approval_requests = req_instance.find_total_no_of_requests()

    withdraw_requests_list = __get_withdrawn_requests_list(req_instance)
    registration_requests_list = __get_registration_request_list(req_instance)
    modification_requests_list = __get_modification_request_list(req_instance)

    return {
        "total_approval_requests": total_approval_requests,
        "withdrawn_requests": withdraw_requests_list,
        "new_registration_requests": registration_requests_list,
        "modification_requests": modification_requests_list,
    }


def __get_withdrawn_requests_list(req_instance):
    withdrawn_requests = req_instance.check_for_withdraw_requests()
    withdraw_requests_list = []

    for request in withdrawn_requests:
        withdrawn_request = {
            "request_id": request[0],
            "user_id": request[1],
            "debited_amount": request[3],
            "date": request[4],
            "requested_by": request[5],
        }
        withdraw_requests_list.append(withdrawn_request)

    return withdraw_requests_list


def __get_registration_request_list(req_instance):
    new_registration_requests = req_instance.check_for_new_registration_request()
    new_registration_requests_list = []

    for request in new_registration_requests:
        registration_request = {
            "user_id": request[0],
            "name": request[1],
            "email": request[2],
            "phone_no": request[3],
            "id_proof_type": request[4],
            "id_proof": request[5],
            "gender": request[6],
            "created_at": request[8],
        }
        new_registration_requests_list.append(registration_request)

    return new_registration_requests_list


def __get_modification_request_list(req_instance):
    modification_requests = req_instance.check_for_user_modification_request()
    modification_requests_list = []

    for request in modification_requests:
        modification_request = {
            "request_id": request[0],
            "user_id": request[1],
            "attribute_to_update": request[2],
            "attribute_value": request[3],
        }
        modification_requests_list.append(modification_request)

    return modification_requests_list


@router.put("/account/requests")
@validate(all_requests_schema)
@role_based_access(["Manager"])
def handle_requests(request: Request, body_data=Body()):
    request_type = body_data["request_type"]

    req_instance = RequestsHandler()
    req_instance.find_total_no_of_requests()

    if request_type == "withdrawn_request":
        response = __update_withdrawn_request(req_instance, body_data=body_data)
        return response

    elif request_type == "registration_request":
        response = __update_registration_request(req_instance, body_data=body_data)
        return response

    elif request_type == "modification_request":
        response = __update_modification_request(req_instance, body_data=body_data)
        return response

    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Request Type")


@validate(withdrawn_request_schema)
def __update_withdrawn_request(req_instance, body_data):
    request_id = body_data["request_id"]
    comment = body_data["comment"]
    request_status = body_data["status"]

    # print(request_id, comment, request_status)

    withdrawn_requests = req_instance.check_for_withdraw_requests()
    response = __handle_withdrawn_requests(
        req_instance, withdrawn_requests, request_id, request_status, comment
    )
    return response


@validate(registration_request_schema)
def __update_registration_request(req_instance, body_data):
    user_id = body_data["user_id"]
    request_status = body_data["status"]

    new_registration_requests = req_instance.check_for_new_registration_request()
    response = __handle_new_registration_requests(
        req_instance, new_registration_requests, user_id, request_status
    )
    return response


@validate(modification_request_schema)
def __update_modification_request(req_instance, body_data):
    request_id = body_data["request_id"]
    request_status = body_data["status"]

    modification_requests = req_instance.check_for_user_modification_request()
    response = __handle_modification_requests(
        req_instance, modification_requests, request_id, request_status
    )
    return response


def __handle_withdrawn_requests(
    req_instance, withdrawn_requests, request_id, request_status, comment
):
    if withdrawn_requests:
        is_valid_withdrawn_request = False

        for request in withdrawn_requests:
            withdrawn_request_id = request[0]
            if withdrawn_request_id != request_id:
                continue
            is_valid_withdrawn_request = True
            user_id = request[1]
            amount = request[3]
            done_by = request[5]

            if request_status == "approved":
                req_instance.approve_withdrawn_request(
                    user_id, amount, done_by, withdrawn_request_id, comment
                )
                return valid_response(200, "Request Approved Successfully.")

            elif request_status == "rejected":
                req_instance.reject_withdrawn_request(
                    user_id, amount, withdrawn_request_id, comment
                )
                return valid_response(200, "Request Rejected Successfully.")

        if not is_valid_withdrawn_request:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, error_response(400, "Request ID not Found")
            )
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            error_response(404, "withdrawn requests not found"),
        )


def __handle_new_registration_requests(
    req_instance, new_registration_requests, user_id, request_status
):
    if new_registration_requests:
        is_valid_user_id = False

        for user in new_registration_requests:
            request_user_id = user[0]

            if request_user_id == user_id:
                is_valid_user_id = True
                req_instance.approve_or_reject_registeration_request(
                    request_user_id, request_status
                )
                return valid_response(200, f"Request {request_status} Successfully.")

        if not is_valid_user_id:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                error_response(
                    404, "User ID not found. Please verify user id and try again."
                ),
            )

    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            error_response(404, "New Registration Requests Not Found."),
        )


def __handle_modification_requests(
    req_instance, modification_requests, request_id, request_status
):
    if modification_requests:
        is_valid_request_id = False

        for request in modification_requests:
            modification_request_id = request[0]
            if modification_request_id != request_id:
                continue
            is_valid_request_id = True
            user_id = request[1]
            attribute_to_update = request[2]
            attribute_value = request[3]

            req_instance.approve_or_reject_modification_requests(
                attribute_to_update,
                attribute_value,
                user_id,
                modification_request_id,
                request_status,
            )
            return valid_response(
                200, f"Modification Request {request_status} Successfully."
            )

        if not is_valid_request_id:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                error_response(
                    404, "Request ID not found. please verify request id and try again."
                ),
            )
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            error_response(404, "Modification Requests Not Found."),
        )
