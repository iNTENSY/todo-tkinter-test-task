import os
import db as database

from handlers import BaseApp


class App(BaseApp):
    TITLE: str = 'Daily Tasks'
    WIDTH: int = 600
    HEIGHT: int = 400
    DEFAULT_COLOR: str = '#1C1C1C'

    def __init__(self):
        super().__init__()
        self.db = database.Database()
        self.title(self.TITLE)
        self['bg'] = self.DEFAULT_COLOR
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.resizable(False, False)
        self.set_all_widgets()


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db = database.Database()
        db.create_database()
        db.close()
    app = App()
    app.mainloop()
