from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions.show import *
from functions.search import *
from functions.delete import *
from functions.add import *
from functions.update import *
from config import *
from functions.save_data import *
from menu_windows.window_help import WindowHelp
from menu_windows.window_filtersort import WindowFilterSort
from menu_windows.window_search import WindowSearch
from menu_windows.window_add import WindowAdd
from menu_windows.window_update import WindowUpdate
import csv
import pandas as pd
import socket
from io import StringIO

server_address = ('localhost', 4999)

SIZE = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

def send_file():
    new_file = pd.read_csv(FILE_PATH)
    new_file = new_file.to_csv(index=False).strip('\n').split('\n')
    new_file_string = '\r\n'.join(df)

    s.send(new_file_string.encode('utf8'))
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

def recv_file():
    message = s.recv(SIZE)
    message = message.decode()
    new_file = pd.read_csv(StringIO(message), sep=',')
    new_file.to_csv(FILE_PATH)

recv_file()

if get_temp_path() == None:
    create_temp()

df = pd.read_csv(get_temp_path())
shown_df = df.head(50)
shown_columns = COLUMNS_IN_SHOW
shown_widths = WIDTHS_IN_SHOW
table = None


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def update_shown_df(data=df, shown_cols=COLUMNS_IN_SHOW, shown_w=WIDTHS_IN_SHOW, update_data=False):
    global window, table, shown_df, shown_columns, shown_widths, df
    if update_data:
        df = pd.read_csv(get_temp_path())
    shown_df = data if not update_data else df
    shown_columns = shown_cols
    shown_widths = shown_w
    table.destroy()
    table.create(window, shown_df, shown_columns, shown_widths)


class Table():

    def __init__(self, root, data, headers, widths):
        self.create(root, data, headers, widths)

    def create(self, root, data, headers, widths):
        self.canvas = Canvas(root)
        frame = ttk.Frame(self.canvas)
        self.frame_head = ttk.Frame(root)

        self.v_scroll = ttk.Scrollbar(
            root, orient='vertical', command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(
            root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.canvas.configure(xscrollcommand=self.h_scroll.set)

        self.frame_head.pack(side=TOP, fill=X)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=frame, anchor="nw")

        self.canvas.bind("<Configure>", lambda event,
                   canvas=self.canvas: onFrameConfigure(self.canvas))

        total_rows = len(data.index)
        if total_rows > 50:
            total_rows = 50

        # code for creating table
        for i, header in enumerate(headers):
            self.e = ttk.Entry(
                self.frame_head, width=widths[i], font=('Montserrat Medium', 11))

            self.e.grid(row=0, column=i, sticky='n')
            self.e.insert(END, header.title())

        for i in range(total_rows):
            for j, header in enumerate(headers):
                self.e = ttk.Entry(frame, width=widths[j],
                                   font=('Montserrat', 11))

                self.e.grid(row=i+1, column=j)
                self.e.insert(END, data.iloc[i][header])

    def destroy(self):
        self.canvas.destroy()
        self.frame_head.destroy()
        self.v_scroll.destroy()
        self.h_scroll.destroy()


def darkstyle(root):
    root.tk.call('source', 'theme/azure.tcl')
    root.tk.call('set_theme', 'dark')


def main_window():
    window = Tk()
    window.geometry('1080x720+100+32')
    window.title("NYC Housing Admin")
    window.resizable(False, False)
    darkstyle(window)

    title_font = ('Montserrat Bold', 24)
    title = ttk.Label(window, text='NYC Housing Admin', font=title_font)
    title.pack(side=TOP, pady=16)

    return window


def create_menu(root):
    frame = ttk.Frame(root)
    frame.pack(side=TOP, pady=32)

    # menu_width = 10
    help_button = ttk.Button(
        master=frame, command=func_help, text="Help")
    show_button = ttk.Button(
        master=frame, command=func_filtersort, text="Sort Data")
    search_button = ttk.Button(
        master=frame, command=func_search, text="Search")
    add_button = ttk.Button(master=frame, command=func_add,
                            text="Add")
    update_button = ttk.Button(
        master=frame, command=func_update, text="Update")
    delete_button = ttk.Button(
        master=frame, command=func_delete, text="Delete")
    save_button = ttk.Button(
        master=frame, command=func_save, text="Save Changes")
    exit_button = ttk.Button(
        master=frame, command=func_exit, text="Exit")

    for i, widget in enumerate(frame.winfo_children()):
        widget.grid(row=0, column=i, padx=8, pady=5, sticky='nesw')


def create_table(root):
    global table
    table = Table(root, shown_df, shown_columns, shown_widths)


def func_help():
    global window
    WindowHelp(window).grab_set()


def func_filtersort():
    global window
    WindowFilterSort(window, df, update_shown_df).grab_set()


def func_search():
    global window
    WindowSearch(window, df, update_shown_df).grab_set()


def func_add():
    global window
    WindowAdd(window, df, update_shown_df).grab_set()


def func_update():
    global window
    WindowUpdate(window, df, update_shown_df).grab_set()


def func_delete():
    pass


def func_save():
    if has_unsaved_changes():
        save()
        send_file()
        messagebox.showinfo(message='Saved Successfully!')
    else:
        messagebox.showinfo(message='No Unsaved Changes')


def func_exit():
    if has_unsaved_changes():
        should_save = messagebox.askyesnocancel(
            title='Warning', message='Save Changes?')
        if should_save == None:
            return
        elif should_save:
            save()
            send_file()
    destroy_temp()
    window.destroy()
    quit()


# Main Window
window = main_window()
window.protocol('WM_DELETE_WINDOW', func_exit)

# Content
create_menu(window)
create_table(window)

if __name__ == '__main__':
    window.mainloop()
    s.close()
