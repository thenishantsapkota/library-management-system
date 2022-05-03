import typing as t


class CustomResponse:
    @staticmethod
    def success(data, message: str) -> dict[str, t.Any]:
        return {"success": True, "data": data, "message": message}
