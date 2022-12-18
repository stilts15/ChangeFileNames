import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from natsort import os_sorted

gui = tk.Tk()
gui.title('Bulk Rename Tool')
gui.geometry('700x800+375+50')
gui.resizable(False, False)

logo = Image.open('GUI_logo2.png')
resize_logo = logo.resize((100, 100))
img = ImageTk.PhotoImage(resize_logo)
label1 = Label(image=img)
label1.image = img
label1.place(relx=0.03, rely=0.85)

author = Label(text='By: Bart Friese', font='System 14 bold')
author.place(relx=0.18, rely=0.918)


class GUI:

    def __init__(self):

        # GET DIRECTORY INTERFACE
        self.directory_label = Label(gui,
                                     text='Directory: ')
        self.directory_label.place(relx=0.02,
                                   rely=0.05)

        self.browse_button = ttk.Button(gui,
                                        command=self.get_folder_path,
                                        text="Browse...")
        self.browse_button.place(relx=0.84,
                                 rely=0.05)

        self.directory_path = Entry(gui,
                                    textvariable=folderPath,
                                    width=53)
        self.directory_path.place(relx=0.12,
                                  rely=0.05)

        # DIRECTORY CONTENTS INTERFACE
        self.directory_contents = Label(gui,
                                        text='Directory contents')
        self.directory_contents.place(relx=0.14,
                                      rely=0.13)

        self.files_to_rename = Label(gui,
                                     text='Files to rename')
        self.files_to_rename.place(relx=0.70,
                                   rely=0.13)

        self.directory_file_list = Listbox(gui,
                                           listvariable=fileslist,
                                           height=20,
                                           selectmode=EXTENDED,
                                           width=30)
        self.directory_file_list.place(relx=0.03,
                                       rely=0.16)

        self.rename_file_list = Listbox(gui,
                                        height=20,
                                        selectmode=EXTENDED,
                                        width=30)
        self.rename_file_list.place(relx=0.58,
                                    rely=0.16)

        self.add_button = ttk.Button(gui,
                                     command=self.add_to_file_list,
                                     text='In >>>',
                                     width=6)
        self.add_button.place(relx=0.43,
                              rely=0.31)

        self.remove_button = ttk.Button(gui,
                                        command=self.remove_from_file_list,
                                        text='<<< Out',
                                        width=6)
        self.remove_button.place(relx=0.43,
                                 rely=0.36)

        # CHOOSE RENAME FUNCTION INTERFACE
        self.add_prefix = ttk.Radiobutton(gui,
                                          command=self.enable_disable_selections,
                                          text='Add prefix',
                                          value='Prefix',
                                          variable=radiobutton,
                                          width=10)
        self.add_prefix.place(relx=0.03,
                              rely=0.65)

        self.add_suffix = ttk.Radiobutton(gui,
                                          command=self.enable_disable_selections,
                                          text='Add suffix',
                                          value='Suffix',
                                          variable=radiobutton,
                                          width=10)
        self.add_suffix.place(relx=0.2,
                              rely=0.65)

        self.rename = ttk.Radiobutton(gui,
                                      command=self.enable_disable_selections,
                                      text='Rename',
                                      value='Rename',
                                      variable=radiobutton,
                                      width=10)
        self.rename.place(relx=0.37,
                          rely=0.65)

        self.enumerate_option = ttk.Checkbutton(gui,
                                                command=self.enable_disable_selections,
                                                text='Enumerate', onvalue='Enumerate',
                                                offvalue='None',
                                                variable=enumeratebutton,
                                                width=10)
        self.enumerate_option.place(relx=0.03,
                                    rely=0.71)
        self.enumerate_option.config(state='disabled')

        separators_list = ['Select Separator',
                           'No Separator',
                           'Space',
                           'Dash',
                           'Dash + Space',
                           'Underscore']

        self.separators_box = ttk.OptionMenu(gui, separatorbutton, *separators_list)
        self.separators_box.place(relx=0.52,
                                  rely=0.6465)

        self.separators_box_enum = ttk.OptionMenu(gui, separatorbutton_enum, *separators_list)
        self.separators_box_enum.place(relx=0.2,
                                       rely=0.7065)
        self.separators_box_enum.config(state='disabled')

        # RENAME INTERFACE
        self.enter_rename_text_label = Label(gui,
                                             text='New text: ')
        self.enter_rename_text_label.place(relx=0.02,
                                           rely=0.77)

        self.rename_text = Entry(gui,
                                 width=53)
        self.rename_text.place(relx=0.12,
                               rely=0.77)

        self.rename_button = ttk.Button(gui,
                                        command=lambda: self.rename_files(),
                                        text="Rename")
        self.rename_button.place(relx=0.84,
                                 rely=0.77)

    def get_folder_path(self):
        folder_selected = filedialog.askdirectory(mustexist=True)
        folderPath.set(folder_selected)
        if not folder_selected:
            return None
        else:
            files = [f for f in os.listdir(folder_selected)
                     if not f.startswith('.')
                     if not f.startswith('~')
                     if os.path.isfile(os.path.join(folder_selected, f))]
            files = os_sorted(files)
            fileslist.set(files)

    def add_to_file_list(self):
        if len(self.directory_file_list.curselection()) != 0:
            all_items = self.directory_file_list.get(0, END)
            selected_items_add = [all_items[item] for item in self.directory_file_list.curselection()]
            for i in selected_items_add:
                self.rename_file_list.insert(END, i)
            selected_items_delete = self.directory_file_list.curselection()
            for n in selected_items_delete[::-1]:
                self.directory_file_list.delete(n)

    def remove_from_file_list(self):
        if len(self.rename_file_list.curselection()) != 0:
            all_items2 = self.rename_file_list.get(0, tk.END)
            selected_items_add2 = [all_items2[item] for item in self.rename_file_list.curselection()]
            for i in selected_items_add2:
                self.directory_file_list.insert(END, i)
            selected_items_delete2 = self.rename_file_list.curselection()
            for n in selected_items_delete2[::-1]:
                self.rename_file_list.delete(n)

    def rename_files(self):
        separator_dict = {'Select Separator': '',
                          'No Separator': '',
                          'Space': ' ',
                          'Dash': '-',
                          'Dash + Space': ' - ',
                          'Underscore': '_'}
        x = separator_dict[separatorbutton.get()]
        y = separator_dict[separatorbutton_enum.get()]
        directory_path = self.directory_path.get()
        new_text = self.rename_text.get()
        count = 0
        if radiobutton.get() == 'Prefix':
            if enumeratebutton.get() == 'Enumerate':
                for file in self.rename_file_list.get(0, END):
                    count += 1
                    current_name = os.path.join(directory_path, file)
                    new_name = os.path.join(directory_path, new_text + x + os.path.splitext(file)[0] + y + str(count) + os.path.splitext(file)[1])
                    os.rename(current_name, new_name)
                self.rename_file_list.delete(0, END)
            else:
                for file in self.rename_file_list.get(0, END):
                    current_name = os.path.join(directory_path, file)
                    new_name = os.path.join(directory_path, new_text + x + file)
                    os.rename(current_name, new_name)
                self.rename_file_list.delete(0, END)
        if radiobutton.get() == 'Suffix':
            if enumeratebutton.get() == 'Enumerate':
                for file in self.rename_file_list.get(0, END):
                    count += 1
                    current_name = os.path.join(directory_path, file)
                    new_name = os.path.join(directory_path, os.path.splitext(file)[0] + x + new_text + y + str(count) + os.path.splitext(file)[1])
                    os.rename(current_name, new_name)
                self.rename_file_list.delete(0, END)
            else:
                for file in self.rename_file_list.get(0, END):
                    current_name = os.path.join(directory_path, file)
                    new_name = os.path.join(directory_path, os.path.splitext(file)[0] + x + new_text + os.path.splitext(file)[1])
                    os.rename(current_name, new_name)
                self.rename_file_list.delete(0, END)
        if radiobutton.get() == 'Rename':
            if separatorbutton_enum.get() == 'Select Separator':
                messagebox.showerror(title='No separator', message='Error: You did not select a separator')
                return None
            else:
                for file in self.rename_file_list.get(0, END):
                    count += 1
                    current_name = os.path.join(directory_path, file)
                    new_name = os.path.join(directory_path, new_text + y + str(count) + os.path.splitext(file)[1])
                    os.rename(current_name, new_name)
            self.rename_file_list.delete(0, END)

    def enable_disable_selections(self):
        if radiobutton.get() == 'Prefix':
            self.separators_box.config(state='normal')
            self.enumerate_option.config(state='normal')
            if enumeratebutton.get() == 'Enumerate':
                self.separators_box_enum.config(state='normal')
            elif enumeratebutton.get() == 'None':
                self.separators_box_enum.config(state='disabled')
        elif radiobutton.get() == 'Suffix':
            self.separators_box.config(state='normal')
            self.enumerate_option.config(state='normal')
            if enumeratebutton.get() == 'Enumerate':
                self.separators_box_enum.config(state='normal')
            elif enumeratebutton.get() == 'None':
                self.separators_box_enum.config(state='disabled')
        elif radiobutton.get() == 'Rename':
            self.separators_box.config(state='disabled')
            enumeratebutton.set('Enumerate')
            self.enumerate_option.config(state='disabled')
            self.separators_box_enum.config(state='normal')


# Variables for variable text
folderPath = StringVar()
fileslist = StringVar()
radiobutton = StringVar()
enumeratebutton = StringVar()
separatorbutton = StringVar()
separatorbutton_enum = StringVar()

start = GUI()

gui.mainloop()
