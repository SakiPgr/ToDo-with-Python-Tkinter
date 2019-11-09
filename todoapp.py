#! python3
# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from tkinter import ttk

task_file = 'tasks.txt'
if not os.path.exists('tasks.txt'):
    with open('tasks.txt', 'w') as f:
        json.dump("[]", f)


class TaskGUI:

    def __init__(self, master):
        self.master = master
        master.title('Tkinter GUI')

        window_width = master.winfo_reqwidth()
        window_height = master.winfo_reqheight()

        master_position_right = int(master.winfo_screenwidth() / 2 - 500 / 2)
        master_position_down = int(master.winfo_screenheight() / 2 - 300 / 2)

        popup_position_right = int(master.winfo_screenwidth() / 2 - window_width / 2)
        popup_position_down = int(master.winfo_screenheight() / 2 - window_height / 2)

        master.geometry('500x340+{}+{}'.format(master_position_right, master_position_down))

        def read_tasks():
            with open('tasks.txt', 'r') as fi:
                tasks = json.load(fi)
            return tasks

        task_list = read_tasks()

        def add_task():
            for i in range(len(task_list)):
                task_number = tk.Label(lower_frame, text=str(i + 1) + '.')
                task_number.grid(column=0, row=i, padx=(5, 0), pady=(10, 0), sticky='w')
                new_task = tk.Label(lower_frame, text=task_list[i][1], anchor='w')
                new_task.grid(column=1, row=i, pady=(10, 0), sticky='we', columnspan=2)
                task_priority = tk.Label(lower_frame, text=task_list[i][0], anchor='e')
                task_priority.grid(column=2, row=i, sticky='ew', pady=(10, 0), padx=(5, 5))
                delete_button = tk.Button(lower_frame, text='Delete', command=lambda name=i: delete_task(name))
                delete_button.grid(column=3, row=i, sticky='e', pady=(10, 0))
                check_done = tk.Checkbutton(lower_frame)
                check_done.grid(column=4, row=i, sticky='e', pady=(10, 0))

        def delete_task(name):
            task_list.pop(name)
            slaves = lower_frame.grid_slaves()
            for i in slaves:
                i.destroy()
            write_task_file()
            add_task()

        def check_entries():
            no_task_and_entry_message = "Please enter a correct task and priority"
            no_task_message = "Please enter a correct task"
            no_priority_message = 'Please enter a correct priority'
            priority = priority_entry.get()
            task = task_entry.get()
            priority_is_int = priority.isdigit()
            if not priority and not task:
                wrong_input(no_task_and_entry_message)
            elif not task:
                wrong_input(no_task_message)
            elif not priority:
                wrong_input(no_priority_message)
            elif not priority_is_int:
                wrong_input(no_priority_message)
            elif priority_is_int:
                if int(priority) > 100 or int(priority) < 1:
                    wrong_input(no_priority_message)
                else:
                    get_entry(priority, task)

        def wrong_input(message):
            win = tk.Toplevel()
            win.wm_title("Problem")
            win.geometry('+{}+{}'.format(popup_position_right, popup_position_down))

            problem = tk.Label(win, text=message)
            problem.grid(row=0, column=0, padx=(5, 5))

            close_window = ttk.Button(win, text="Okay", command=win.destroy)
            close_window.grid(row=1, column=0, pady=(3, 3))

        def get_entry(priority, task):
            task_list.append([priority, task])
            priority_entry.delete(0, 'end')
            task_entry.delete(0, 'end')
            task_list.sort()
            write_task_file()
            add_task()

        def write_task_file():
            with open(task_file, 'w') as fi:
                json.dump(task_list, fi)

        upper_frame = tk.Frame(master)
        upper_frame.pack(side=tk.TOP, fill=tk.BOTH)

        task_label = tk.Label(upper_frame, text='Please enter your task')
        task_label.pack(fill=tk.X)
        task_entry = tk.Entry(upper_frame)
        task_entry.pack(fill=tk.X, padx=5)

        priority_label = tk.Label(upper_frame, text='Please enter the tasks priority (1 up to 100)')
        priority_label.pack(fill=tk.X)
        priority_entry = tk.Entry(upper_frame)
        priority_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        change_task = tk.Button(upper_frame, text="Add Task", command=check_entries)
        change_task.config(width=20)
        change_task.pack(side=tk.BOTTOM, pady=(0, 5))

        sep = ttk.Separator(window, orient='horizontal', style='Line.TSeparator')
        sep.pack(fill='x')

        bottom_frame = tk.Frame(window)
        bottom_frame.pack(side=tk.BOTTOM, fill='both')

        lower_frame = tk.Frame(window)
        lower_frame.pack(side=tk.BOTTOM, fill='both', expand=1)
        lower_frame.grid_columnconfigure(1, weight=3)

        add_task()

        quit_button = tk.Button(bottom_frame, text='Quit', width=20, command=window.destroy)
        quit_button.pack(side='left', pady=(0, 5), padx=(5, 0))
        ok_button = tk.Button(bottom_frame, text='OK', width=20)  # need to add command
        ok_button.pack(side='right', pady=(0, 5), padx=(0, 5))


window = tk.Tk()
myGui = TaskGUI(window)

if __name__ == '__main__':
    window.mainloop()
