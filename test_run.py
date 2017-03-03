from sanic.utils import sanic_endpoint_test
from runtime import jieba_apiserver_app_runapp


def test_endpoint_homepage():
    request, response = sanic_endpoint_test(
            jieba_apiserver_app_runapp, uri='/api'
            )
    print(response.status)
    assert response.status == 200
