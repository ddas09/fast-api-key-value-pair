from enum import Enum


class AppConstants:
    class ResponseStatusEnum(Enum):
        Success = "success"
        Created = "created"
        Conflict = "conflict"
        NotFound = "not_found"
        BadRequest = "bad_request"
        ServerError = "server_error"

    SERVER_ERROR_MESSAGE = "Something went wrong. Internal server error!"
