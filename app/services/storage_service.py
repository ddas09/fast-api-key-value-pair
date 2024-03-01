import redis
from app.models.key_value_model import KeyValueModel
from app.common.constants.app_constants import AppConstants
from app.common.exceptions.api_exception import ApiException

redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)


class StorageService:
    def add_value(self, data: KeyValueModel):
        key_str = str(data.key)
        if redis_client.exists(key_str):
            raise ApiException(
                f"Value with Key '{data.key}' already exists.",
                AppConstants.ResponseStatusEnum.Conflict,
            )

        redis_client.set(key_str, data.value)

    def update_value(self, data: KeyValueModel):
        key_str = str(data.key)
        if not redis_client.exists(key_str):
            raise ApiException(
                f"Can't update, key '{data.key}' not found.",
                AppConstants.ResponseStatusEnum.NotFound,
            )

        redis_client.set(key_str, data.value)

    def delete_value(self, key: int):
        key_str = str(key)
        if not redis_client.exists(key_str):
            raise ApiException(
                f"Can't delete, key '{key}' not found.",
                AppConstants.ResponseStatusEnum.NotFound,
            )

        redis_client.delete(key)

    def get_value(self, key: int):
        key_str = str(key)
        value = redis_client.get(key_str)
        if value is None:
            raise ApiException(
                f"Value with key '{key}' not found.",
                AppConstants.ResponseStatusEnum.NotFound,
            )

        return value
