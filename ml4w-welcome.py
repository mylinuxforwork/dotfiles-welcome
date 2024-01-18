#  __  __ _    _  ___        __     _    _                 _   
# |  \/  | |  | || \ \      / /    / \  | |__   ___  _   _| |_ 
# | |\/| | |  | || |\ \ /\ / /    / _ \ | '_ \ / _ \| | | | __|
# | |  | | |__|__   _\ V  V /    / ___ \| |_) | (_) | |_| | |_ 
# |_|  |_|_____| |_|  \_/\_/    /_/   \_\_.__/ \___/ \__,_|\__|
                                                             
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
@Gtk.Template(filename='src/welcome.ui')

# -----------------------------------------
# Main Window
# -----------------------------------------
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'Ml4wWelcomeWindow'

    # Get objects from template
    ml4w_version = Gtk.Template.Child()
    update_banner = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -----------------------------------------
# Main App
# -----------------------------------------
class MyApp(Adw.Application):

    # Path to home folder
    homeFolder = os.path.expanduser('~')
    current_version_name = ""
    current_version_code = ""

    def __init__(self, **kwargs):
        super().__init__(application_id='com.ml4w.welcome',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
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

        # Check dotfiles version
        self.readDotfilesVersion(win)

        # Show Application Window
        print(":: Show Main Window")
        win.present()

        # Check for updates
        self.checkForUpdates(win)

    def checkForUpdates(self,win):
        print(":: Check for updates")
        try:
            result = subprocess.run(["bash", self.homeFolder + "/dotfiles/.version/update.sh"], capture_output=True, text=True)
            web_version = result.stdout.strip()
            print("Update " +  web_version)
            if (web_version == '0'):
                print("Show update banner")
                win.update_banner.set_revealed(True)
        except:
            print("ERROR: Could not read the file /dotfiles/.version/update.sh")

    def readDotfilesVersion(self,win):
        print(":: Get dotfiles version")
        try:
            result = subprocess.run(["bash", self.homeFolder + "/dotfiles/.version/version.sh"], capture_output=True, text=True)
            print("Version " +  result.stdout)
            version = result.stdout
            version_arr = version.split(" ")
            self.current_version_name = version_arr[0]
            self.current_version_code = version_arr[1]
            win.ml4w_version.set_text("Version: " + self.current_version_name)
        except:
            print("ERROR: Could not read the file /dotfiles/.version/version.sh")
            win.ml4w_version.set_text("")

    def on_about(self, widget, _):
        dialog = Adw.AboutWindow(
            application_icon="application-x-executable",
            application_name="ML4W Welcome",
            developer_name="Stephan Raabe",
            version="1.0.0",
            website="https://gitlab.com/stephan-raabe/dotfiles",
            issue_url="https://gitlab.com/stephan-raabe/dotfiles/-/issues",
            support_url="https://gitlab.com/stephan-raabe/dotfiles/-/issues",
            copyright="© 2024 Stephan Raabe",
            license_type=Gtk.License.GPL_3_0_ONLY
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