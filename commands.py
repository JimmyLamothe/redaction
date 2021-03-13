""" Testing module for Tkinter commands

Constants:
    HANDLED_EVENT_LIST
    TRACKED_EVENT_LIST
    UNTRACKED_EVENT_LIST
    IGNORED_EVENT_LIST

Functions:
    print_tracked_events(Root)
    print_event(tkinter.Event)
"""

import tkinter as tk

#Events that have at least one event handler configured
HANDLED_EVENT_LIST = [
    '<Configure>',
    '<KeyPress>',
    '<KeyRelease>',
    '<ButtonRelease>',
]

#Events that are printed out to the console
TRACKED_EVENT_LIST = [
    '<KeyPress>',
]

#Other Tkinter events that can be tracked
UNTRACKED_EVENT_LIST = [
    '<Activate>',
    '<Destroy>',
    '<Map>',
    '<ButtonPress>',
    '<Enter>',
    '<FocusIn>',
    '<MouseWheel>',
    '<FocusOut>',
    '<Property>',
    '<Configure>',
    '<Unmap>',
    '<Create>',
    '<Leave>',
    '<Visibility>',
    '<Deactivate>',

]

#Tkinter events that are never tracked
IGNORED_EVENT_LIST = [
    '<Motion>',
    '<Expose>',
    '<Colormap>',
    '<MapRequest>',
    '<CirculateRequest>',
    '<ResizeRequest>',
    '<ConfigureRequest>',
    '<Gravity>',
    '<Reparent>',
    '<Circulate>',
]

def print_tracked_events(root):
    """ Prints tracked event info when triggered | None -> None """
    for event in TRACKED_EVENT_LIST:
        root.bind(event, print_event)

def print_event(event):
    """ Print even info | None -> None """
    print(event)
    print(event.__dict__)
