import tkinter as tk

#Events that have at least one event handler configured
HANDLED_EVENT_LIST = [
    '<Configure>',
]

#Events that are printed out to the console
TRACKED_EVENT_LIST = [
    '<KeyPress>',
    '<KeyRelease>',
]

#Other Tkinter events that can be tracked
UNTRACKED_EVENT_LIST = [
    '<Activate>',
    '<Destroy>',
    '<Map>',
    '<ButtonPress>',
    '<Enter>',
    '<ButtonRelease>',
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
    for event in TRACKED_EVENT_LIST:
        root.bind(event, print_event)

def print_event(event):
    print(event)
    print(event.__dict__)
