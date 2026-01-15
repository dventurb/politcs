import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk 
from window import create_window

def main():
    app = Gtk.Application(application_id="org.gtk.politcs")
    app.connect("activate", create_window)

    style_provider = Gtk.CssProvider()
    style_provider.load_from_path("assets/css/style.css")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    app.run(None)

if __name__ == "__main__":
    main()
