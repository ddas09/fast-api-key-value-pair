from fastapi import status
from typing import Any, Optional
from fastapi.responses import JSONResponse
from app.models.api_response_model import ApiResponseModel
from app.common.constants.app_constants import AppConstants


class ResponseBuilder:
    @staticmethod
    def _build_response_payload(
        status_code: int,
        status: AppConstants.ResponseStatusEnum,
        message: str,
        data: Any = None,
    ):
        if data is not None and hasattr(data, "__dict__"):
            data = data.__dict__

        response_content = ApiResponseModel(
            data=data, status=status.value, message=message
        )
        return JSONResponse(content=response_content.__dict__, status_code=status_code)

    def success(self, message: str, data: any = None):
        return self._build_response_payload(
            status.HTTP_200_OK, AppConstants.ResponseStatusEnum.Success, message, data
        )

    def created(self, message: str, data: any = None):
        return self._build_response_payload(
            status.HTTP_201_CREATED,
            AppConstants.ResponseStatusEnum.Created,
            message,
            data,
        )

    def conflict(self, message: str):
        return self._build_response_payload(
            status.HTTP_409_CONFLICT, AppConstants.ResponseStatusEnum.Conflict, message
        )

    def not_found(self, message: str):
        return self._build_response_payload(
            status.HTTP_404_NOT_FOUND, AppConstants.ResponseStatusEnum.NotFound, message
        )

    def bad_request(self, message: str):
        return self._build_response_payload(
            status.HTTP_400_BAD_REQUEST,
            AppConstants.ResponseStatusEnum.BadRequest,
            message,
        )

    def server_error(self):
        return self._build_response_payload(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            AppConstants.ResponseStatusEnum.ServerError,
            AppConstants.SERVER_ERROR_MESSAGE,
        )
