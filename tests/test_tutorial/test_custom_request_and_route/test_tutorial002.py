from dirty_equals import IsDict, IsOneOf
from fastapi.testclient import TestClient

from docs_src.custom_request_and_route.tutorial002 import app

client = TestClient(app)


def test_endpoint_works():
    response = client.post("/", json=[1, 2, 3])
    assert response.json() == 6


def test_exception_handler_body_access():
    response = client.post("/", json={"numbers": [1, 2, 3]})
    assert response.json() == IsDict(
        {
            "detail": {
                "errors": [
                    {
                        "type": "list_type",
                        "loc": ["body"],
                        "msg": "Input should be a valid list",
                        "input": {"numbers": [1, 2, 3]},
                    }
                ],
                # httpx 0.28.0 switches to compact JSON https://github.com/encode/httpx/issues/3363
                "body": IsOneOf('{"numbers": [1, 2, 3]}', '{"numbers":[1,2,3]}'),
            }
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": {
                # httpx 0.28.0 switches to compact JSON https://github.com/encode/httpx/issues/3363
                "body": IsOneOf('{"numbers": [1, 2, 3]}', '{"numbers":[1,2,3]}'),
                "errors": [
                    {
                        "loc": ["body"],
                        "msg": "value is not a valid list",
                        "type": "type_error.list",
                    }
                ],
            }
        }
    )
