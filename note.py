from datetime import date
from db_connect import cursor as c
from typing import Tuple, Optional
from user import User


class Note:

    def __init__(self, title: str, author: User, p_date: date, content: str):
        self.title: str = title
        self.author: User = author
        self.publish_date: date = p_date
        self.content: str = content

    @property
    def note_id(self) -> Optional[int]:
        c.execute("SELECT noteID FROM Notes "
                  "WHERE title = '{}' AND authorID = '{}' AND content = '{}'"
                  .format(self.title, self.author.user_id, self.content))
        got: Tuple[int] = c.fetchone()
        if got is None:
            print("This note is not in Notes Table!")
            return None
        return got[0]

    def __repr__(self):
        header = "Note {} created by {} {}, published on {}\n". \
            format(self.title, self.author.name, self.author.surname,
                   self.publish_date)
        return header + "-" * int(len(header) * 0.75) + "\n" + self.content





