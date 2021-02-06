import mysql.connector
from note import Note
from datetime import date
from typing import List, Tuple


db_connection = mysql.connector.connect(host="sql7.freesqldatabase.com",
                                        user="sql7390966",
                                        password="5IwvBd1nzd",
                                        database="sql7390966")
c = db_connection.cursor()


def create_notes_table():
    c.execute("CREATE TABLE Notes ("
              "noteID int PRIMARY KEY AUTO_INCREMENT,"
              "title VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_slovak_ci,"
              "author VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_slovak_ci,"
              "published_date DATE,"
              "content VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_slovak_ci"
              ")")


def drop_table(table: str):
    try:
        c.execute("DROP TABLE {}".format(table))
    except mysql.connector.errors.ProgrammingError:
        print("Dropping table with name '{}' has failed!".format(table))
        return
    print("Drop was sucessful!")


def insert_note(note: Note):
    try:
        c.execute("INSERT INTO Notes (title, author, published_date, content)"
                  "VALUES"
                  "('{}', '{}', '{}', '{}')".
                  format(note.title, note.author, str(note.publish_date),
                         note.content)
                  )
        db_connection.commit()
    except mysql.connector.errors.ProgrammingError:
        print("Insertion failed!")
        return
    print("Succesfully inserted!")


def delete_all_notes(table: str = "Notes"):
    try:
        c.execute("DELETE FROM {}".format(table))
        db_connection.commit()
    except mysql.connector.errors.ProgrammingError:
        print("Deletion of all rows has failed!")
        return
    print("Deletion of all rows succeeded")


def delete_note_by_id(note_id: int, table: str = "Notes"):
    c.execute("SELECT * FROM Notes WHERE noteID = {}".format(note_id))
    if c.fetchone() is None:
        print("No record inside Notes table with noteID equals {}!".
              format(note_id))
        return

    try:
        c.execute("DELETE FROM {} WHERE noteID = {}".format(table, note_id))
        db_connection.commit()
    except mysql.connector.errors.ProgrammingError:
        print("Deletion by note_id has failed!")
        return
    print("Deletion by note_id succedeed!")


def select_whole_table(table: str = "Notes") \
        -> List[Tuple[str, str, date, str]]:
    c.execute("SELECT * FROM {}".format(table))
    return c.fetchall()


# nakupne_polozky = "- milk\n- eggs\n- salt"
# note1 = Note("Shopping", "Marek Nagy", date(2021, 1, 5), nakupne_polozky)
# insert_note(note1)
# print(select_whole_table())











