#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from io import BytesIO
from unittest.mock import patch

import pytest
from urllib3.response import HTTPResponse
from urllib3.util.retry import RequestHistory, Retry

import kaggle_brane as kb


@pytest.fixture
def api() -> None:
    from kaggle.api.kaggle_api_extended import KaggleApi

    _api = KaggleApi()
    _api.authenticate()
    return _api


def _handle_request(pool, method, url, body=None, headers=None, **kwargs):
    if (method, url, kwargs["fields"]) == (
        "GET",
        "https://www.kaggle.com/api/v1/competitions/list",
        [("group", ""), ("category", ""), ("sortBy", ""), ("page", 1), ("search", "")],
    ):
        body = "{}"
        return HTTPResponse(body=body.encode("utf-8"), headers=headers, status=200)

    if (method, url, kwargs["fields"]) == (
        "GET",
        "https://www.kaggle.com/api/v1/competitions/data/download-all/test-comp",
        [],
    ):
        body = "i am data"
        body = body.encode("utf-8")
        if not hasattr(body, "read"):
            body = BytesIO(body)
        else:
            body.seek(0)

        content_len = body.getbuffer().nbytes
        print(content_len)
        location = "https://storage.googleapis.com/kaggle-competitions-data/kaggle-v2/6768/44342/bundle/archive.zip?GoogleAccessId=x&Expires=1622746390&Signature=x&response-content-disposition=attachment%3B+filename%3Dweb-traffic-time-series-forecasting.zip"

        headers.update({"location": location})
        headers.update({"content-length": str(content_len)})

        response = HTTPResponse(
            body=body,
            headers=headers,
            retries=Retry(
                status=200,
                history=[
                    RequestHistory(method, url, None, 200, redirect_location=location,)
                ],
            ),
            preload_content=False,
            status=200,
        )
        return response

    print("pool:", pool)
    print("method:", method)
    print("url:", url)
    print("body:", body)
    print("headers:", headers)
    print("kwargs:", kwargs)

    raise ValueError("unknown REST api call")


@patch("urllib3.poolmanager.PoolManager.request", _handle_request)
def test_list_competitions_with_unspecified_competition(api) -> None:
    env = dict()
    success, output, error = kb.list_competitions(api, env)
    print("success:", success)
    print("output:", output)
    print("error:", error)
    assert not success
    assert "specify competition" in error


@patch("urllib3.poolmanager.PoolManager.request", _handle_request)
def test_list_competitions(api) -> None:
    env = dict(COMPETITION="test-comp")
    success, output, error = kb.list_competitions(api, env)
    print("success:", success)
    print("output:", output)
    print("error:", error)
    assert success
    assert error == ""


@patch("urllib3.poolmanager.PoolManager.request", _handle_request)
def test_download_competitions(api) -> None:
    comp = "test-comp"
    with tempfile.TemporaryDirectory(prefix="kaggle-challenge") as dest:
        env = dict(COMPETITION=comp, DESTINATION=dest)
        success, output, error = kb.download_competition(api, env)
        print("success:", success)
        print("output:", output)
        print("error:", error)
        outfile = os.path.join(dest, comp + ".zip")
        assert os.listdir(dest) == [comp + ".zip"]
        print(outfile)
        with open(outfile, "rb") as f:
            assert f.read() == "i am data".encode("utf-8")
        assert success
        assert error == ""
