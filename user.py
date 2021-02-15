from db_connect import cursor as c
from typing import Tuple, Optional


class User:

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    @property
    def user_id(self) -> Optional[int]:
        c.execute("SELECT userID FROM Users "
                  "WHERE name = '{}' AND surname = '{}'"
                  .format(self.name, self.surname))
        got: Tuple[int] = c.fetchone()
        if got is None:
            print("This user is not in Users table!")
            return None
        return got[0]

    def __repr__(self):
        return "User: {} {}, id = {}".format(self.name, self.surname,
                                             self.user_id)
