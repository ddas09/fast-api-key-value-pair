import logging
from fastapi import Request
from app.helpers.response_builder import ResponseBuilder
from app.common.constants.app_constants import AppConstants
from app.common.exceptions.api_exception import ApiException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class GlobalExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
            return response

        except Exception as exception:
            logging.exception("An exception occurred:")
            return await self._handle_exception(exception)

    async def _handle_exception(self, exception: Exception):
        response_builder = ResponseBuilder()

        if isinstance(exception, ApiException):
            response = self._handle_api_exception(exception, response_builder)

        else:
            response = response_builder.server_error()

        return response

    def _handle_api_exception(self, exception: ApiException, response_builder: ResponseBuilder):
        message = str(exception)
        status = exception.error_code

        if status == AppConstants.ResponseStatusEnum.Conflict:
            return response_builder.conflict(message)

        elif status == AppConstants.ResponseStatusEnum.NotFound:
            return response_builder.not_found(message)

        elif status == AppConstants.ResponseStatusEnum.BadRequest:
            return response_builder.bad_request(message)

        else:
            return response_builder.server_error()
