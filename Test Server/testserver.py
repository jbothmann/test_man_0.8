import os

from flask import Flask, json

DIR =  "C:/Users/np0083/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    @app.route('/')
    def manifest():
        return json.jsonify({'app': 'Power Tools Test Manager', 'version': '0.8'})

    @app.route('/index')
    def index():
        with open(DIR+'dummy index.json') as f:
            return json.jsonify(json.load(f))

    @app.route('/station/<url>')
    def serveStation(url):
        if url == '1111111111111111':
            with open(DIR+'dummy 1.json') as f:
                return json.jsonify(json.load(f))
        elif url == '2222222222222222':
            with open(DIR+'dummy 2.json') as f:
                return json.jsonify(json.load(f))
        elif url == '3333333333333333':
            with open(DIR+'dummy 3.json') as f:
                return json.jsonify(json.load(f))
        return 'default'

    return app

app = create_app()
app.run()
