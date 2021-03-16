from flask import Flask, session
from flask_restful import Api, Resource, request
from flask_db import db, UserModel
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

login_error_message = {
    'success': False,
    'message': "Username or password is invalid."
    }

@app.before_first_request
def create_table():
    db.create_all()

class LoginView(Resource):
    # used for login
    def put(self):
        input_json = json.loads(request.get_data().decode('UTF-8'))
        username = input_json['username']
        password = input_json['password']

        user = UserModel.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return {
                'success': True,
                'id': user.id
                }
        else:
            return login_error_message
    
    @login_required
    def delete(self):
        logout_user()
        return {
            'message': 'You are now logged out.'
        }
    
    # used for register
    def post(self):
        input_json = json.loads(request.get_data().decode('UTF-8'))
        print("Received JSON: {}".format(input_json))
        username = input_json['username']
        password = input_json['password']

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            user = UserModel(username, password)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return {
                'success': True,
                'id': user.id
                }
        else:
            return login_error_message

# # class NoteView(Resource):
# #     def put(self):
# #         input_json = request.get_data()
# #         title = input_json["title"]
# #         body = input_json["body"]

# #         note = NoteModel.query.filter_by(title=title).first()

# #         if note is None:
# #             note = NoteModel(title, body)
# #         else:
# #             note.update(body)
        
# #         db.session.add(note)
# #         db.session.commit()

# #         return note.json()

# # api.add_resource(NoteView, '/note')

api.add_resource(LoginView, '/login')

if __name__ == "__main__":
    app.secret_key = os.urandom(64)
    app.run(host="localhost", port=5000, debug=True)