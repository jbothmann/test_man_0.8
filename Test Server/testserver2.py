import os

from flask import Flask, json, request

#DIR =  "D:/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/"
DIR = "C:/Users/np0083/Documents/GitHub/test_man_0.8/Test Server/dummy JSON/"

class Polling():
    def __init__(self):
        self.api = Flask(__name__, instance_relative_config=True)
        self.api.config.from_mapping(SECRET_KEY='dev')
        self.api.add_url_rule('/', 'manifest', self.manifest)
        self.api.add_url_rule('/index', 'index', self.index)
        self.api.add_url_rule('/station/<url>', 'serve station', self.serveStation)
        self.api.add_url_rule('/shutdown', 'shutdown', self.shutdown)

    def mainloop(self):
        self.api.run(host='0.0.0.0')

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def manifest(self):
        return json.jsonify({'app': 'Power Tools Test Manager', 'version': '0.8'})

    def index(self):
        with open(DIR+'dummy index.json') as f:
            return json.jsonify(json.load(f))

    def serveStation(self, url):
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

    def shutdown(self):
        self.shutdown_server()
        return 'Server shutting down...'

    

if __name__ == '__main__':
    poll = Polling()
    poll.mainloop()