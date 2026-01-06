import azure.functions as func
from function_app import http_trigger

import azure.functions as func
from function_app import http_trigger

def test_http_trigger_with_query_param():
    req = func.HttpRequest(
        method="GET",
        url="/api/http_trigger",
        params={"name": "Victor"},
        body=None
    )

    resp = http_trigger(req)

    assert resp.status_code == 200
    assert b"Hello, Victor" in resp.get_body()


def test_http_trigger_with_json_body():
    req = func.HttpRequest(
        method="POST",
        url="/api/http_trigger",
        params={},
        body=b'{"name": "Blob"}'
    )

    resp = http_trigger(req)

    assert resp.status_code == 200
    assert b"Hello, Blob" in resp.get_body()


def test_http_trigger_without_name():
    assert True