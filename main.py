import mysql.connector
from note import Note
from datetime import date
from typing import List, Tuple, Optional


class NotesTable:
    pass


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


def select_note_by_id(note_id: int, table: str = "Notes") -> Optional[Note]:
    try:
        c.execute("SELECT * FROM {} WHERE noteID = {}".format(table, note_id))
        got: Tuple[str, str, date, str] = c.fetchone()
        if got is None:
            print("Table '{}' doesnt contain a record with id {}".
                  format(table, note_id))
            return
        return Note(got[0], got[1], got[2], got[3])
    except mysql.connector.errors.ProgrammingError:
        print("Selection failed due to unknown error!")
        return


def draw_whole_table(table: str = "Notes"):
    records_lst: List[Tuple[str, str, date, str]] = select_whole_table(table)
    print("-" * 76)
    print("| {:6} | {:^20} | {:^20} | {:^10} | {:256}"
          .format("noteID", "title", "author", "published", "content"))
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


def change_note_by_id(note_id: int, new_title: str = None,
                      new_author: str = None, new_date: date = None,
                      new_content: str = None):
    if new_title is not None and len(new_title) > 20:
        print("Lenght of new_title exceeded the maximum varchar!")
    if new_author is not None and len(new_author) > 20:
        print("Length of new_author exceeded the maximum varchar!")
    if new_content is not None and len(new_content) > 256:
        print("Length of new_content exceeded the maximum varchar!")

    try:
        c.execute("SELECT * FROM Notes WHERE noteID = {}".format(note_id))
        record: Tuple[str, str, date, str] = c.fetchone()
        new_title = new_title if new_title is not None else record[1]
        new_author = new_author if new_author is not None else record[2]
        new_date = new_date if new_date is not None else record[3]
        new_date = str(new_date)
        new_content = new_content if new_content is not None else record[4]
        c.execute("UPDATE Notes SET "
                  "title = '{}',"
                  "author = '{}',"
                  "published_date = '{}',"
                  "content = '{}'"
                  "WHERE noteID = {}"
                  .format(new_title, new_author, new_date, new_content,
                          note_id))
        print("Update was succesfull!")
    except mysql.connector.errors.ProgrammingError:
        print("Update has failed!")
        return


nakupne_polozky = "- milk\n- eggs\n- salt"
note1 = Note("Shopping", "Marek Nagy", date(2021, 1, 5), nakupne_polozky)
# insert_note(note1)
# print(select_whole_table())
# draw_whole_table()

# change_note_title_by_id(28, "Shopping")
change_note_by_id(28, new_title="Shopping45", new_author="Random", new_date=date(1999, 1, 1), new_content="Hello World!")



