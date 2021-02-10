import tkinter as tk

class Key(tk.Entry):
    def __init__(self, master):
        tk.Entry.__init__(
            self,
            master=master,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE'
        )

    def get_contents(self):
        key_list = self.get().split(' ')
        key_list = [key for key in key_list if not key == '']
        return key_list
