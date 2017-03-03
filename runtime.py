from sanic import Sanic
from jieba_apiserver_app.core_view.index import main


jieba_apiserver_app_runapp = Sanic(__name__)
jieba_apiserver_app_runapp.blueprint(main)

if __name__ == "__main__":
    jieba_apiserver_app_runapp.run(host="0.0.0.0", port=8000, debug=True)
