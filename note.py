from datetime import date


class Note:

    def __init__(self, title: str, author: str, p_date: date,
                 content: str):
        self.title = title
        self.author = author
        self.publish_date = p_date
        self.content = content

    def __repr__(self):
        header = "{} note, published by {} on {}\n".format(self.title,
                                                           self.author,
                                                           self.publish_date)
        content = "\n{}".format(self.content)
        return header + ("-" * int((len(header) * 0.75))) + content + "\n"


if __name__ == "__main__":
    nakupne_polozky = "- milk\n- eggs\n- salt"
    note1 = Note("Shopping", "Marek Nagy", date(2021, 1, 5),
                 nakupne_polozky)
    print(note1)
    print(str(note1.publish_date))

