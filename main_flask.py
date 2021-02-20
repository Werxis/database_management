from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
from databases import FileSystemDatabase

db = FileSystemDatabase()

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class DateTime(Resource):
	def get(self):
		dt = datetime.now()
		return { 'date': {
				'day': dt.day,
				'month': dt.month,
				'year': dt.year
				},
			'time': {
				'hour': dt.hour,
				'minute': dt.minute,
				'second': dt.second
				}
			}

class Login(Resource):
	def put(self):
		pass

api.add_resource(HelloWorld, "/")
api.add_resource(DateTime, "/datetime")
api.add_resource(Login, "/login")

if __name__ == '__main__':
	# try:
    app.run(host='0.0.0.0', debug=True)
	# finally:
	# 	db.close_and_zip()

