import os
import sys
from hurry.filesize import size as sizef
import tkinter as tk
from tkinter import filedialog

class Sizr(tk.Frame):
    current_dir = "."

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.file_list = None
        self.size_list = None
        self.current_dir = self.gen_dialog_box()
        self.size_window()


    def get_size(self, start_path='.'):
        total_size = 0
        for root, dirs, files in os.walk(start_path, topdown=False):
            for name in files:
                fp = os.path.join(root, name)
                if not os.path.islink(fp):
                    try:
                        size = os.path.getsize(fp)
                        total_size += size
                    except:
                        pass
        return total_size

    def get_each_folder_size(self, start_path="."):
        all_files = [f for f in os.listdir(start_path)]
        files_with_sizes = []
        for file in all_files:
            if not os.path.isfile(file):
                size = self.get_size(os.path.join(start_path, file))
                files_with_sizes.append((file, size))
            else:
                size = os.path.getsize(file)
                files_with_sizes.append((file, size))

        return files_with_sizes

    def sort_files(self, files):
        def sorting_method(file):
            return file[1]
        return files.sort(reverse=True, key=sorting_method)

    def gen_size_window_scroll(self):
        scrollbar = tk.Scrollbar(self)
        # scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        scrollbar.grid(row=0,column=2, rowspan=3, sticky="ns")

        self.file_list = tk.Listbox(self, yscrollcommand = scrollbar.set)
        self.size_list = tk.Listbox(self, yscrollcommand = scrollbar.set)
        files = self.get_each_folder_size(self.current_dir)
        self.sort_files(files)
        for filename, size in files:
            self.file_list.insert(tk.END, filename)
            self.size_list.insert(tk.END, sizef(size))

        # self.file_list.pack(side=tk.TOP, fill = tk.BOTH)
        self.file_list.grid(row=1, column=0, sticky=tk.E)
        # self.size_list.pack(side=tk.TOP, fill = tk.BOTH)
        self.size_list.grid(row=1, column=1, sticky=tk.E)
        scrollbar.config(command = self.scroll)

    def scroll(self, *args):
        self.file_list.yview(*args)
        self.size_list.yview(*args)


    def size_window_create_label(self, left_text, right_text):
        self.label = tk.Label(self)
        self.label['text'] = left_text
        # self.label.pack(side="top")
        self.label.grid(row=0, column=0)
        self.label = tk.Label(self)
        self.label['text'] = right_text
        # self.label.pack(side="top")
        self.label.grid(row=0, column=1)

    def size_window(self):
        self.size_window_create_label("Filename", "Size")
        self.gen_size_window_scroll()

    def gen_dialog_box(self):
        return filedialog.askdirectory()


if __name__ == "__main__":
    root = tk.Tk()
    app = Sizr(master=root)
    app.mainloop()
