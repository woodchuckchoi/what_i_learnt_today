# flask_restplus library automatically generates Swagger man pages.

from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    def post(self):
        return {'hello': 'post'}
if __name__ == '__main__':
    app.run(debug=True)
