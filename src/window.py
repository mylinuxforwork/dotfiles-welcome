from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/ml4w/welcome/window.ui')
class DotfilesWelcomeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DotfilesWelcomeWindow'

    ml4w_version = Gtk.Template.Child()
    ml4w_folder = Gtk.Template.Child()
    update_banner = Gtk.Template.Child()
    btn_toggle = Gtk.Template.Child()
    switch_autostart = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
