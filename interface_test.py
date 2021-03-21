""" Main module for Key/Phrase. Run from the console. """


import tkinter as tk
import config
from Root import Root

root = Root() #Main Key/Phrase Tkinter program
root.bind_events(test=True)

root.mainloop()
