from db_connect import db_connection, cursor as c
from mysql.connector.errors import ProgrammingError, IntegrityError, \
    DatabaseError
from note import Note
from user import User
from datetime import date
from typing import List, Tuple, Optional, Union

Note_record = Tuple[int, str, int, date, str]
User_record = Tuple[int, str, str]


class TableUtils:

    def __init__(self):
        pass

    @staticmethod
    def create_users_table() -> None:
        try:
            c.execute(
                "CREATE TABLE Users ("
                "userID int PRIMARY KEY AUTO_INCREMENT,"
                "name VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_slovak_ci,"
                "surname VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_slovak_ci"
                ")"
            )
            print("Table was created succesfully!")
        except (ProgrammingError, DatabaseError):
            print("Creation of table Users has failed!")
            return

    @staticmethod
    def create_notes_table() -> None:
        q = """CREATE TABLE Notes (
               noteID int AUTO_INCREMENT,
               title VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_slovak_ci,
               authorID int,
               published_date DATE,
               content VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_slovak_ci,
               PRIMARY KEY (noteID),
               FOREIGN KEY (authorID) REFERENCES Users (userID)
               )"""
        try:
            c.execute(q)
            print("Table was created succesfully!")
        except DatabaseError:
            print("Cannot create Notes Table before Users table is created,"
                  " because of foreign key constraints!")
            return

    @staticmethod
    def drop_table(table: str) -> None:
        try:
            c.execute("DROP TABLE {}".format(table))
            print("Drop was sucessful!")
        except ProgrammingError:
            print("Dropping table with name '{}' has failed!".format(table))
            return
        except IntegrityError:
            print("Cannot delete or update a parent row: "
                  "a foreign key constraint fails")
            return

    @staticmethod
    def clear_table(table: str) -> None:
        try:
            c.execute("DELETE FROM {}".format(table))
            db_connection.commit()
        except ProgrammingError:
            print("Deletion of all rows has failed!")
            return
        print("Deletion of all rows succeeded")

    @staticmethod
    def select_whole_table(table: str) -> \
            Union[List[User_record], List[Note_record]]:
        c.execute("SELECT * FROM {}".format(table))
        return c.fetchall()

    @staticmethod
    def insert_user(user: User) -> None:
        try:
            c.execute(
                "INSERT INTO Users (name, surname)"
                "VALUES"
                "('{}', '{}')".format(user.name, user.surname)
            )
            db_connection.commit()
        except ProgrammingError:
            print("Insertion of a given user into Users table has failed!")
            return
        print("Succesfully inserted into Users table!")

    @staticmethod
    def delete_user_by_id(user_id: int, table: str = "Users") -> None:
        c.execute("SELECT * FROM Users WHERE userID = {}".format(user_id))
        if c.fetchone() is None:
            print("No record inside Users table with userID equals {}!"
                  .format(user_id))
            return

        try:
            c.execute(
                "DELETE FROM {} WHERE userID = {}".format(table, user_id)
            )
            db_connection.commit()
            print("Deletion by user_id succedeed!")
        except ProgrammingError:
            print("Deletion by user_id has failed!")
            return
        except IntegrityError:
            print("Cannot delete or update a parent row: "
                  "a foreign key constraint fails")
            return

    @staticmethod
    def change_user_by_id(user_id: int, new_name: str = None,
                          new_surname: str = None) -> None:
        if new_name is not None and len(new_name) > 20:
            print("new_name length is over 20 characters!!")
            return
        if new_surname is not None and len(new_surname) > 20:
            print("new_surname length is over 20 characters!!")
            return

        c.execute("SELECT * FROM Users WHERE userID = {}".format(user_id))
        record: Tuple[int, str, str] = c.fetchone()
        if record is None:
            print("User with given ID is not in Users table!")
            return
        new_name = new_name if new_name is not None else record[1]
        new_surname = new_surname if new_surname is not None else record[2]
        try:
            c.execute("UPDATE Users SET "
                      "name = '{}',"
                      "surname = '{}'"
                      "WHERE userID = {}"
                      .format(new_name, new_surname, user_id))
            db_connection.commit()
            print("Update was succesfull!")
        except ValueError:
            print("Update of user with id {} failed!".format(user_id))
            return

    @staticmethod
    def select_user_by_id(user_id: int, table: str = "Users") \
            -> Optional[User]:
        try:
            c.execute("SELECT * FROM {} WHERE userID = {}"
                      .format(table, user_id))
            got: Tuple[int, str, str] = c.fetchone()
            if got is None:
                print("Table {} doesnt contain record with user id: {}"
                      .format(table, user_id))
                return
            return User(got[1], got[2])
        except ProgrammingError:
            print("Selection failed!")
            return

    @staticmethod
    def draw_whole_users_table() -> None:
        try:
            records: List[User_record] = TableUtils.select_whole_table("Users")
        except ProgrammingError:
            print("Cannot draw users table, it probably even doesnt exist!")
            return

        print("-" * (6+20+20 + 4+3+3))
        print("| {:6} | {:^20} | {:^20} |".format("userID", "name", "surname"))
        print("-" * (6 + 20 + 20 + 4 + 3 + 3))
        for record in records:
            print("| ", end="")
            print("{:^6} ".format(record[0]), end="")
            print("| ", end="")
            print("{:^20} ".format(record[1]), end="")
            print("| ", end="")
            print("{:^20} ".format(record[2]), end="")
            print("|")
            print("-" * (6 + 20 + 20 + 4 + 3 + 3))

    @staticmethod
    def insert_note(note: Note) -> None:
        if note.author.user_id is None:
            print("Cannot insert given note, author is not in Users table!")
            return
        try:
            c.execute(
                "INSERT INTO Notes (title, authorID, published_date, content)"
                "VALUES"
                "('{}', '{}', '{}', '{}')"
                .format(note.title, note.author.user_id,
                        str(note.publish_date), note.content)
            )
            db_connection.commit()
        except ProgrammingError:
            print("Insertion of a note into Notes table has failed!\n")
            return
        print("Succesfully inserted into Notes table!")

    @staticmethod
    def delete_note_by_id(note_id: int, table: str = "Notes") -> None:
        c.execute("SELECT * FROM Notes WHERE noteID = {}".format(note_id))
        if c.fetchone() is None:
            print("No record inside Notes table with noteID equals {}!".
                  format(note_id))
            return

        try:
            c.execute(
                "DELETE FROM {} WHERE noteID = {}".format(table, note_id)
            )
            db_connection.commit()
        except ProgrammingError:
            print("Deletion by note_id has failed!")
            return
        print("Deletion by note_id succedeed!")

    @staticmethod
    def change_note_by_id(note_id: int, new_title: str = None,
                          new_auth: User = None, new_date: date = None,
                          new_content: str = None) -> None:
        if new_title is not None and len(new_title) > 20:
            print("Lenght of new_title exceeded the maximum varchar!")
            return
        if new_auth is not None and new_auth.user_id is None:
            print("This user is not in Users table, cannot be used!")
            return
        if new_content is not None and len(new_content) > 256:
            print("Length of new_content exceeded the maximum varchar!")
            return

        try:
            c.execute("SELECT * FROM Notes WHERE noteID = {}"
                      .format(note_id))
            record: Tuple[int, str, User, date, str] = c.fetchone()
            if record is None:
                print("No note record found with given noteID!")
                return
            new_title = new_title if new_title is not None else record[1]
            new_auth_id = new_auth.user_id if new_auth is not None else \
                record[2]
            new_date = new_date if new_date is not None else record[3]
            new_date = str(new_date)
            new_content = new_content if new_content is not None else record[4]
            c.execute("UPDATE Notes SET "
                      "title = '{}',"
                      "authorID = '{}',"
                      "published_date = '{}',"
                      "content = '{}'"
                      "WHERE noteID = {}"
                      .format(new_title, new_auth_id, new_date,
                              new_content, note_id)
                      )
            print("Update was succesfull!")
            db_connection.commit()
        except ProgrammingError:
            print("Update has failed!")
            return

    @staticmethod
    def select_note_by_id(note_id: int, table: str = "Notes") \
            -> Optional[Note]:
        try:
            c.execute("SELECT * FROM {} WHERE noteID = {}"
                      .format(table, note_id))
            got: Tuple[int, str, int, date, str] = c.fetchone()
            if got is None:
                print("Table '{}' doesnt contain a record with id {}!".
                      format(table, note_id))
                return
            c.execute("SELECT * FROM Users where userID = {}".format(got[2]))
            user_got = c.fetchone()
            usr = User(user_got[1], user_got[2])
            return Note(got[1], usr, got[3], got[4])
        except ProgrammingError:
            print("Selection failed due to unknown error!")
            return

    @staticmethod
    def draw_whole_notes_table() -> None:
        try:
            records_lst: List[Tuple[int, str, int, date, str]] = \
                TableUtils.select_whole_table("Notes")
        except ProgrammingError:
            print("Cannot draw Notes table, it probably doesnt even exist!")
            return

        print("-" * 76)
        print("| {:6} | {:^20} | {:^20} | {:^10} | {:256}"
              .format("noteID", "title", "authorID", "published", "content"))
        print("-" * 76)
        for record in records_lst:
            print("| ", end="")
            print("{:^6} ".format(record[0]), end="")
            print("| ", end="")
            print("{:^20} ".format(record[1]), end="")
            print("| ", end="")
            print("{:^20} ".format(record[2]), end="")
            print("| ", end="")
            print("{:^10} ".format(str(record[3])), end="")
            print("| ", end="")
            print("{:256}".format(record[4].replace("\n", "\n" + " "*70)))
            print("-" * 76)


if __name__ == "__main__":
    usr1 = User("Marián", "Svitek")
    usr2 = User("Marek", "Nagy")
    note1 = Note("Shopping", usr2, date(2021, 2, 14), "eggs\nmilk\nwater")

    # TableUtils.create_users_table()   # must be first, before Notes, foreign
    # TableUtils.create_notes_table()
    # TableUtils.insert_user(usr1)
    # TableUtils.insert_user(usr2)
    # TableUtils.insert_note(note1)
    # TableUtils.change_user_by_id(1, new_name="Jozef", new_surname=None)
    # user1: User = TableUtils.select_user_by_id(1)
    # user2: User = TableUtils.select_user_by_id(2)
    # nt1: Note = TableUtils.select_note_by_id(1)
    # TableUtils.change_note_by_id(1, new_title="To_shop", new_auth=user1)
    # TableUtils.delete_note_by_id(1)
    # TableUtils.delete_user_by_id(1)
    # TableUtils.clear_table("Users")
    # TableUtils.clear_table("Notes")
    # TableUtils.draw_whole_users_table()
    # TableUtils.draw_whole_notes_table()
    # TableUtils.drop_table("Notes")
    # TableUtils.drop_table("Users")
