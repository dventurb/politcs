import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk 

from game import init_game

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

def create_window(app):
    window = Gtk.ApplicationWindow(application=app, title="Politcs")
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    box.get_style_context().add_class("box")
    window.set_child(box)

    init_game(box)

    window.present()
