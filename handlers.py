import tkinter as tk

from windows import EditWindow, DeleteWindow


# noinspection PyTypeChecker
class WidgetHandler:
    TITLE: str = 'title'
    DEFAULT_COLOR = None

    def set_all_widgets(self):
        self.frame = tk.Frame(
            self,
            bg='#4A4A4A',
            height=250,
            width=300
        )
        self.title_label = tk.Label(
            self,
            text=self.TITLE,
            font='Arial 20 bold',
            bg=self.DEFAULT_COLOR,
            fg='white'
        )
        self.entry = tk.Entry(
            self.frame,
            justify='left',
            font='Arial 13 bold',
            bg='#707070',
            fg='white',
            width=50
        )
        self.scrollbar = tk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=lambda *args: self.listbox.yview(*args)
        )
        self.listbox = tk.Listbox(
            self.frame,
            listvariable=tk.Variable(value=self.get_all_tasks()),
            selectmode=tk.EXTENDED,
            yscrollcommand=self.scrollbar.set,
            width=40
        )
        self.add_button = tk.Button(
            self,
            command=self.add_task,
            text='Добавить',
            fg='#fff',
            bg='#08f',
            width=60
        )
        self.delete_button = tk.Button(
            self,
            command=self.delete_selected_tasks,
            text='Удалить',
            fg='#fff',
            bg='#08f',
            width=60
        )
        self.edit_button = tk.Button(
            self,
            text='Редактировать запись',
            fg='#fff',
            bg='#08f',
            width=60,
            command=self.edit_task
        )

        self.title_label.pack(side='top', pady=30)
        self.frame.pack()
        self.entry.grid(pady=1, row=0, column=0, sticky='we')
        self.listbox.grid(row=1, column=0, columnspan=2, sticky='nwe')
        self.scrollbar.grid(row=0, column=2, rowspan=2, sticky='ns')
        self.add_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.edit_button.pack(pady=5)

    def get_selected_tasks(self):
        """
        Данный метод возвращает наименования всех
        выделенных объектов.
        """
        result = self.listbox.curselection()
        objects_list = [self.listbox.get(i) for i in result]
        return objects_list


class BackendHandler:
    def add_task(self):
        """
        Данный метод предоставляет
        возможность добавления данных в БД.
        """
        task = self.entry.get()
        if task.strip() == '':
            return
        self.db.push_data(title=(task,))
        self.listbox.insert(0, task)
        self.entry.delete(0, tk.END)

    def delete_selected_tasks(self):
        """
        Данный метод предоставляет
        возможность удаления данных из БД.
        """
        selected_list = self.get_selected_tasks()
        w = DeleteWindow(master=self, db=self.db, objects=selected_list)
        w.display_window()

    def get_all_tasks(self) -> list[str]:
        """
        Данный метод возвращает список всех задач.
        """
        self.tasks = self.db.get_all_tasks()
        task_titles = [title[0] for title in self.tasks]
        return task_titles

    def edit_task(self):
        selected_obj = self.get_selected_tasks()[0]
        w = EditWindow(master=self, task=selected_obj, db=self.db)
        w.display_window()


class BaseApp(tk.Tk,
              WidgetHandler,
              BackendHandler,
              EditWindow,
              DeleteWindow):
    def refresh(self):
        """
        Данный метод обновляет
        существующие виджеты приложения.
        """
        widgets = self.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.set_all_widgets()
