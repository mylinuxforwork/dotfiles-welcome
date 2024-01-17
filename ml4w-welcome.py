import sys
import gi
import subprocess
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
from gi.repository import GLib
from gi.repository import GObject

# -----------------------------------------
# Define UI template
# -----------------------------------------
@Gtk.Template(filename='welcome.ui')

# -----------------------------------------
# Main Window
# -----------------------------------------
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'Ml4wWelcomeWindow'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -----------------------------------------
# Main App
# -----------------------------------------
class MyApp(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(application_id='com.ml4w.welcome',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.homeFolder = os.path.expanduser('~')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('update', self.on_system_update)
        self.create_action('cleanup', self.on_system_cleanup)
        self.create_action('about', self.on_about)
        self.create_action('settings', self.on_settings)
        self.create_action('waybar_reload', self.on_waybar_reload)
        self.create_action('keybindings', self.on_keybindings)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        
        win.present()

    def on_about(self, widget, _):
        dialog = Adw.AboutWindow(
            application_icon="application-x-executable",
            application_name="Typeset",
            developer_name="Angela Avery",
            version="1.2.3",
            website="https://example.org",
            issue_url="https://example.org",
            support_url="https://example.org",
            copyright="© 2023 Angela Avery",
            license_type=Gtk.License.GPL_3_0_ONLY,
            developers=["Angela Avery <angela@example.org>"],
            artists=["GNOME Design Team"],
        )
        dialog.present()

    def on_settings(self, widget, _):
        print(":: In BTN settings handler")
        subprocess.Popen(["alacritty", "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/hypr/start-settings.sh"])

    def on_system_update(self, widget, _):
        print(":: In BTN system_update handler")
        subprocess.Popen(["alacritty","-e", self.homeFolder + "/dotfiles/scripts/installupdates.sh"])

    def on_system_cleanup(self, widget, _):
        print(":: In BTN system_update handler")
        subprocess.Popen(["alacritty","-e", self.homeFolder + "/dotfiles/scripts/cleanup.sh"])

    def on_waybar_reload(self, widget, _):
        print(":: In BTN waybar_reload handler")
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/waybar/launch.sh"])

    def on_keybindings(self, widget, _):
        print(":: In BTN keybindings handler")
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/hypr/scripts/keybindings.sh"])

    # Add Application actions
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

# -----------------------------------------
# Application Start
# -----------------------------------------
app = MyApp()
app.run(sys.argv)