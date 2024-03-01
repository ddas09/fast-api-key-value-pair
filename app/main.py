from fastapi import FastAPI, Depends
from app.models.key_value_model import KeyValueModel
from app.services.storage_service import StorageService
from app.helpers.response_builder import ResponseBuilder
from app.middlewares.global_exception_handler import GlobalExceptionHandler

app = FastAPI()


def get_storage_service():
    return StorageService()


app.add_middleware(GlobalExceptionHandler)

response_builder = ResponseBuilder()


@app.post("/values")
async def add_value(
    data: KeyValueModel, storage_service: StorageService = Depends(get_storage_service)
):
    storage_service.add_value(data)
    return response_builder.created(message="Value added successfully", data=data)


@app.put("/values")
async def update_value(
    data: KeyValueModel, storage_service: StorageService = Depends(get_storage_service)
):
    storage_service.update_value(data)
    return response_builder.success(message="Value updated successfully", data=data)


@app.get("/values/{key}")
async def read_value(
    key: int, storage_service: StorageService = Depends(get_storage_service)
):
    value = storage_service.get_value(key)
    return response_builder.success(message="Value retrieved successfully", data=value)


@app.delete("/values/{key}")
async def delete_value(
    key: int, storage_service: StorageService = Depends(get_storage_service)
):
    storage_service.delete_value(key)
    return response_builder.success("Value deleted successfully")
