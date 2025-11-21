from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidMaxPriceException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Max price must be greater then 0."
    default_code = "invalid_data"


class InsufficientFundsException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Insufficient balance."
    default_code = "insufficient_funds"


class InvalidOfferStateForCancellationException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Only active offers can be cancelled."
    default_code = "invalid_status"
