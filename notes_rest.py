from flask import Flask, session
from flask_restful import Api, Resource, request
from flask_db import db, UserModel, NoteModel
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
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

register_error_message = {
    'success': False,
    'message': "Username is already being used."
    }

note_not_found_error = {
    'message': "Note not found."
    }, 400

@app.before_first_request
def create_table():
    db.create_all()

class LoginView(Resource):
    # user for testing login
    #@login_required
    def get(self):
        '''
            Used for testing if current user is logged in.
        '''
        return {'logged_in': current_user.is_authenticated}

    # used for login
    def post(self):
        '''
            Login existing user.
            JSON is expected to have "username" and "password" attributes.
        '''
        if current_user.is_authenticated:
            return {'message':'User already logged in.'}

        input_json = json.loads(request.get_data().decode('UTF-8'))
        username = input_json['username']
        password = input_json['password']

        user = UserModel.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return {
                'success': True,
                'id': user.id
                }, 200
        else:
            return login_error_message

class RegisterView(Resource):
    # used for register
    def post(self):
        '''
            Register new user.
            JSON is expected to have "username" and "password" attributes.
        '''
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
            return register_error_message


class LogoutView(Resource):
    @login_required
    def delete(self):
        #print(current_user)
        logout_user()
        return {
            'message': 'You are now logged out.'
        }

class NoteView(Resource):    
    @login_required
    def delete(self):
        input_json = json.loads(request.get_data().decode('UTF-8'))
        id = input_json["id"]

        note = NoteModel.query.filter_by(id=id).first()
        if note is not None:
            db.session.delete(note)
            db.session.commit()
            return {'message': "Note deleted."}
        else:
            return note_not_found_error, 400

    @login_required
    def post(self):
        input_json = json.loads(request.get_data().decode('UTF-8'))
        title = input_json["title"]
        body = input_json["body"]

        note = NoteModel(current_user, title, body)
        
        db.session.add(note)
        db.session.commit()

        return note.json()

class NoteUpdateView(Resource):
    @login_required
    def post(self):
        input_json = json.loads(request.get_data().decode('UTF-8'))
        id = input_json['id']
        title = input_json["title"]
        body = input_json["body"]

        note = NoteModel.query.filter_by(id=id).first()
        if note is not None:
            note.update(title, body)
            db.session.commit()
            return note.json(), 200
        else:
            return note_not_found_error

class NotesView(Resource):
    @login_required
    def get(self):
        '''
            Get all notes of currently logged in user.
        '''
        notes = NoteModel.query.filter_by(user=current_user).all()
        return {
            'notes': list(map(lambda x: x.json(), notes))
        }

api.add_resource(LoginView, '/login')
api.add_resource(LogoutView, '/logout')
api.add_resource(RegisterView, '/register')

api.add_resource(NoteView, '/note')
api.add_resource(NotesView, '/notes')
api.add_resource(NoteUpdateView, '/note/update')

if __name__ == "__main__":
    app.secret_key = os.urandom(64)
    app.run(host="localhost", port=5000, debug=True)