"""
Данный модуль используется для работы
с базой данных данного приложения.
"""
import sqlite3


class Connection:
    def __init__(self):
        self.connect = sqlite3.connect('db.sqlite')
        self.cur = self.connect.cursor()

    def close(self):
        self.connect.close()


class Database(Connection):
    def create_database(self) -> None:
        """
        Метод позволяющий создать базу данных
        """
        q = """
                CREATE TABLE IF NOT EXISTS todos (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task VARCHAR(100) UNIQUE
                );
            """

        self.cur.execute(q)

    def get_all_tasks(self) -> list:
        """
        Данный метод возвращает список всех
        """
        q = """
                SELECT task FROM todos
                ORDER BY id DESC
            """
        result = self.cur.execute(q)
        return list(result)

    def push_data(self, title):
        q = """
                INSERT INTO todos(task) VALUES (?)
            """
        self.cur.execute(q, title)
        self.connect.commit()

    def delete_data(self, values):
        q = """
                DELETE FROM todos WHERE task IN ({});
            """.format(', '.join(['?'] * len(values)))
        self.cur.execute(q, tuple(values))
        self.connect.commit()

    def update(self, new, old):
        q = """
                UPDATE todos
                SET task = ?
                WHERE task == ?
            """
        self.cur.execute(q, [new, old])
        self.connect.commit()
