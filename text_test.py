import tkinter as tk
from AutoText import AutoText
from Key import Key

root = tk.Tk()

class TestText(AutoText):
    def __init__(self, master, **kwargs):
        AutoText.__init__(
            self,
            master,
            height=1,
            width=40,
            relief=tk.RIDGE,
            bg='#FFFFFF', #F5F5F5 in put mode
            borderwidth=2, #3 in put mode
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE'
)

text = TestText(root)
        
text.pack()

root.mainloop()
