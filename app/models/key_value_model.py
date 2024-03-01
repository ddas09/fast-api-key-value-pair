from pydantic import BaseModel, validator
from app.common.constants.app_constants import AppConstants
from app.common.exceptions.api_exception import ApiException


class KeyValueModel(BaseModel):
    key: int
    value: str

    @validator("key")
    def validate_key(cls, value):
        if value <= 0:
            raise ApiException(
                message="Key must be a positive integer", error_code=AppConstants.ResponseStatusEnum.BadRequest)

        return value

    @validator("value")
    def validate_value(cls, value):
        if len(value) < 3:
            raise ApiException(
                message="Value must be at least 3 characters long", error_code=AppConstants.ResponseStatusEnum.BadRequest)

        return value
