import os

from flask import Flask, json


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # a simple page that says hello
    @app.route('/index')
    def index():
        with open('D:/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/dummy index.json') as f:
            return json.jsonify(json.load(f))

    @app.route('/station/<url>')
    def serveStation(url):
        if url == '1111111111111111':
            with open('D:/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/dummy 1.json') as f:
                return json.jsonify(json.load(f))
        elif url == '2222222222222222':
            with open('D:/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/dummy 2.json') as f:
                return json.jsonify(json.load(f))
        elif url == '3333333333333333':
            with open('D:/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/dummy 3.json') as f:
                return json.jsonify(json.load(f))
        return 'default'

    return app

app = create_app()
app.run()
