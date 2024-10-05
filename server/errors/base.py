from __future__ import annotations

from functools import cached_property
from typing import Any

from pydantic import BaseModel


# do not use directly!
class BaseHTTPError(Exception):
    status_code: int
    detail: str
    headers: dict[str, str] | None = None
    _list_of_subclasses: list[type[BaseHTTPError]] = []

    # for mypy only
    class Model(BaseModel):
        detail: str = ""

    # create pydantic model from Exception to handle and return it in `server.errors.handlers`
    def __init_subclass__(cls, **kwargs: Any) -> None:
        name_of_class = kwargs.get("model_name", cls.__name__ + "Model")
        klass = type(
            name_of_class,
            (BaseModel,),
            {
                "detail": cls.detail,
            },
        )

        klass.__annotations__["status_code"] = int
        klass.__annotations__["detail"] = str

        cls.Model = klass  # type: ignore[assignment]

        BaseHTTPError._list_of_subclasses.append(cls)

    @cached_property
    def model(self) -> BaseModel:
        return self.Model()

    @classmethod
    def generate_responses(
        cls, *classes: type[BaseHTTPError]
    ) -> dict[int, dict[str, Any]]:
        if len(classes) == 0:
            classes_to_include = cls._list_of_subclasses
        else:
            classes_to_include = list(set(classes) & set(cls._list_of_subclasses))

        responses = {}

        for error in classes_to_include:
            responses[error.status_code] = {
                "model": error.Model,
                "description": error.detail,
            }

        return responses
