import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk 

from game import init_menu

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

def create_window(app):
    window = Gtk.ApplicationWindow(application=app, title="Politcs")
    window.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    box.get_style_context().add_class("box")
    window.set_child(box)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
    box.append(stack)
    
    init_menu(stack)
    stack.set_visible_child_name("menu")

    window.present()
