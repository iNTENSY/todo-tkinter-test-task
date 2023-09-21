import tkinter as tk

from tkinter import messagebox


class BaseWindow:
    PAGE_TITLE: str = 'tk'

    def __init__(self,
                 width: int = 300,
                 height: int = 100):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self._window_title = self.PAGE_TITLE
        self.window.geometry(f'{width}x{height}')
        self.window.title(self._window_title)

    def display_window(self):
        self.window.mainloop()

    @staticmethod
    def confirmation():
        result = messagebox.askyesno(title='Подтверждение',
                                     message='Подтвердить операцию?')
        if result:
            messagebox.showinfo('Результат', 'Операция выполнена!')
        else:
            messagebox.showerror('Результат', 'Операция отменена!')
        return result


class EditWindow(BaseWindow):
    PAGE_TITLE: str = 'Изменение'

    def __init__(self, master, task: str, db):
        self.master = master
        self.task = task
        self.db = db
        super().__init__()

    def display_window(self):
        frame = tk.Frame(self.window)
        btn_frame = tk.Frame(frame)
        label = tk.Label(frame, text=f'Вы изменяете: {self.task}')
        self.edit_window_entry = tk.Entry(frame, width=40)
        yes_btn = tk.Button(btn_frame,
                            text='Изменить',
                            command=self.do_edit,
                            fg='#fff',
                            bg='#08f')
        cancel_btn = tk.Button(btn_frame,
                               text='Отмена',
                               command=self.window.destroy,
                               fg='#fff',
                               bg='#08f')

        frame.pack(expand=True)
        label.pack()
        self.edit_window_entry.pack(expand=True)
        btn_frame.pack(pady=10)
        yes_btn.grid(row=0, column=0)
        cancel_btn.grid(row=0, column=1, padx=10)

        super().display_window()

    def do_edit(self):
        result: bool = self.confirmation()
        edited_message: str = self.edit_window_entry.get()
        if result:
            self.db.update(new=edited_message, old=self.task)
            self.master.refresh()
        self.window.destroy()


class DeleteWindow(BaseWindow):
    PAGE_TITLE: str = 'Удаление'

    def __init__(self, master, db, objects):
        self.master = master
        self.db = db
        self.objects = objects
        super().__init__()

    def display_window(self):
        frame = tk.Frame(self.window)
        text = f'Количество выбранных записей: {len(self.objects)}'
        label = tk.Label(frame, text=text)
        yes_btn = tk.Button(frame,
                            text=self.PAGE_TITLE,
                            command=self.do_delete,
                            fg='#fff',
                            bg='#08f')
        cancel_btn = tk.Button(frame,
                               text='Отмена',
                               command=self.window.destroy,
                               fg='#fff',
                               bg='#08f')
        frame.pack(expand=True)
        label.grid(row=0, column=0, columnspan=2)
        yes_btn.grid(row=1, column=0)
        cancel_btn.grid(row=1, column=1)

        super().display_window()

    def do_delete(self):
        result = self.confirmation()
        if result:
            self.db.delete_data(values=self.objects)
            self.master.refresh()
        self.window.destroy()
