import pytest
from unittest.mock import patch
from app.models.key_value_model import KeyValueModel
from app.common.exceptions.api_exception import ApiException
from app.services.storage_service import StorageService


@pytest.fixture
def storage_service():
    return StorageService()


@patch("app.services.storage_service.redis_client")
@patch("app.services.storage_service.task_queue")
def test_add_value_success(mock_task_queue, mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.exists.return_value = False
    storage_service.add_value(key_value_data)
    mock_task_queue.enqueue.assert_called_once_with(
        storage_service._set_value, str(key_value_data.key), key_value_data.value
    )


@patch("app.services.storage_service.redis_client")
@patch("app.services.storage_service.task_queue")
def test_add_value_failure_existing_key(
    mock_task_queue, mock_redis_client, storage_service
):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.exists.return_value = True
    with pytest.raises(
        ApiException, match=f"Value with Key '{key_value_data.key}' already exists."
    ):
        storage_service.add_value(key_value_data)
    mock_task_queue.enqueue.assert_not_called()


@patch("app.services.storage_service.redis_client")
def test_update_value_failure_nonexistent_key(mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="UpdatedValue")
    mock_redis_client.exists.return_value = False
    with pytest.raises(
        ApiException, match=f"Can't update, key '{key_value_data.key}' not found."
    ):
        storage_service.update_value(key_value_data)
    mock_redis_client.set.assert_not_called()


@patch("app.services.storage_service.redis_client")
@patch("app.services.storage_service.task_queue")
def test_delete_value_success(mock_task_queue, mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.exists.return_value = True
    storage_service.delete_value(key_value_data.key)
    mock_task_queue.enqueue.assert_called_once_with(
        storage_service._delete_value, str(key_value_data.key)
    )


@patch("app.services.storage_service.redis_client")
def test_delete_value_failure_nonexistent_key(mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.exists.return_value = False
    with pytest.raises(
        ApiException, match=f"Can't delete, key '{key_value_data.key}' not found."
    ):
        storage_service.delete_value(key_value_data.key)
    mock_redis_client.delete.assert_not_called()


@patch("app.services.storage_service.redis_client")
def test_get_value_success(mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.get.return_value = key_value_data.value
    result = storage_service.get_value(key_value_data.key)
    mock_redis_client.get.assert_called_once_with(str(key_value_data.key))
    assert result == key_value_data.value


@patch("app.services.storage_service.redis_client")
def test_get_value_failure_nonexistent_key(mock_redis_client, storage_service):
    key_value_data = KeyValueModel(key=1, value="TestValue")
    mock_redis_client.get.return_value = None
    with pytest.raises(
        ApiException, match=f"Value with key '{key_value_data.key}' not found."
    ):
        storage_service.get_value(key_value_data.key)
    mock_redis_client.get.assert_called_once_with(str(key_value_data.key))
