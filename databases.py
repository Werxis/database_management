import os
import shutil

DB_DIR_NAME = 'database'
# users
USERS_DIR_NAME = 'users'
USERS_FILENAME = 'users.txt'
# notes
NOTES_DIR_NAME = 'users'
NOTES_FILENAME = 'note.txt'
# out
OUT_ZIP_FILENAME = 'db.zip'

class User:
    def __init__(self, name: str, salted_password: str):
        self.username = name
        self.salted_password = salted_password
    
    def get_username(self):
        return self.username

class FileSystemDatabase:
    '''
        Initialize file system based database.
    '''
    def __init__(self):
        if DB_DIR_NAME not in os.listdir():
            os.mkdir(DB_DIR_NAME)
        os.chdir(DB_DIR_NAME)
        # init users directory if neccesary
        init_users()
        init_notes()
    
    def init_users(self):
        if USERS_DIR_NAME not in os.listdir():
            os.mkdir(USERS_DIR_NAME)

        if USERS_FILENAME not in os.listdir(USERS_DIR_NAME):
            with open(os.path.join(USERS_DIR_NAME, USERS_FILENAME), 'w'):
                pass
    
    def init_notes(self):
        if NOTES_DIR_NAME not in os.listdir():
            os.mkdir(NOTES_DIR_NAME)
            
        users = load_users()
        usernames = set(map(lambda x: x.get_username(), users))
        for dir in os.listdir(NOTES_DIR_NAME):
            is_dir = os.path.isdir(os.path.join(NOTES_DIR_NAME, dir))
            is_username = dir in usernames
            if not (is_dir and is_username):
                raise Exception("Unknown directory {}".format(os.path.join(NOTES_DIR_NAME, dir)))
    
    def load_users(self):
        users = set()
        with open(os.path.join(USERS_DIR_NAME, USERS_FILENAME), 'r') as users_file:
            lines = list(map( lambda x: x[:-1], users_file.readlines()))
        for line in lines:
            lineParts = line.split(';')
            users.add(User(lineParts[0], lineParts[1]))
        return users
    
    def close_and_zip(self):
        os.chdir('..')
        shutil.make_archive(OUT_ZIP_FILENAME,
            'zip', '.')
        