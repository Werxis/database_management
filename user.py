from db_connect import cursor as c
from typing import Tuple


class User:

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    @property
    def user_id(self):
        c.execute("SELECT userID FROM Users "
                  "WHERE name = '{}' AND surname = '{}'"
                  .format(self.name, self.surname))
        got: Tuple[int] = c.fetchone()
        return got[0]

    def __repr__(self):
        return "User ID: {}, {} {}".format(self.user_id, self.name, self.surname)


