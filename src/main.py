import sys
import gi
import subprocess
import os
import pathlib
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import DotfilesWelcomeWindow

# Get script path
pathname = os.path.dirname(sys.argv[0])

# The main application singleton class.
class DotfilesWelcomeApplication(Adw.Application):

    homeFolder = os.path.expanduser('~')
    pathname = os.path.dirname(sys.argv[0])
    current_version_name = ""
    current_version_code = ""
    tiling = False
    browser = "firefox"
    terminal = "kitty"
    editor = "gnome-text-editor"
    filemanager = "nautilus"
    networkmanager = "nm-connection-editor"
    app_info = ""

    def __init__(self):
        super().__init__(application_id='com.ml4w.welcome',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('update', self.on_system_update)
        self.create_action('settings', self.on_settings)
        self.create_action('monitors', self.on_monitors)
        self.create_action('sidebar', self.on_sidebar)
        self.create_action('hyprlandsettings', self.on_hyprlandsettings)
        self.create_action('keybindings', self.on_keybindings)
        self.create_action('gitlab', self.on_gitlab)
        self.create_action('youtube', self.on_youtube)
        self.create_action('network', self.on_network)
        self.create_action('bluetooth', self.on_bluetooth)
        self.create_action('howtoupdate', self.on_howtoupdate)
        self.create_action('toggle', self.on_toggle)
        self.create_action('autostart', self.on_autostart)
        self.create_action('hyprlandhomepage', self.on_hyprlandhomepage)
        self.create_action('hyprlandwiki', self.on_hyprlandwiki)
        self.create_action('wallpapers', self.on_wallpapers)
        self.create_action('systeminfo', self.on_system_info)
        self.create_action('sddm_wallpaper', self.on_sddm_wallpaper)
        self.create_action('exit_hyprland', self.on_exit_hyprland)
        self.create_action('update_dotfiles', self.on_update_dotfiles)
        self.create_action('keyboard', self.on_keyboard)
        self.create_action('shell', self.on_shell)
        self.create_action('changelog', self.on_changelog)
        self.create_action('wiki', self.on_wiki)
        self.create_action('uninstall', self.on_uninstall)
        self.create_action('nm-applet-start', self.on_nmapplet_start)

    # Called when the application is activated.
    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DotfilesWelcomeWindow(application=self)

        # Get Autostart Button
        self.switch_autostart = win.switch_autostart
        if (os.path.exists(self.homeFolder + "/.cache/ml4w-welcome-autostart")):
            self.switch_autostart.set_active(False)
        else:
            self.switch_autostart.set_active(True)

        # Get Window Toggle Button
        self.btn_toggle = win.btn_toggle

        # Read configuration
        self.readDotfilesVersion(win)
        self.checkForUpdates(win)
        self.getBrowser()
        self.getTerminal()
        self.getEditor()
        self.getFilemanager()
        self.getNetworkmanager()
        win.present()

    def getTerminal(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/terminal.sh"], capture_output=True, text=True)
            self.terminal = result.stdout.strip()
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/terminal.sh")

    def getBrowser(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/browser.sh"], capture_output=True, text=True)
            self.browser = result.stdout.strip()
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/browser.sh")

    def getEditor(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/editor.sh"], capture_output=True, text=True)
            self.editor = result.stdout.strip()
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/editor.sh")

    def getFilemanager(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/filemanager.sh"], capture_output=True, text=True)
            self.filemanager = result.stdout.strip()
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/filemanager.sh")

    def getNetworkmanager(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/.config/ml4w/settings/networkmanager.sh"], capture_output=True, text=True)
            self.networkmanager = result.stdout.strip()
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/settings/networkmanager.sh")

    def on_update_dotfiles(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "flatpak", "run", "com.ml4w.dotfilesinstaller"])

    def checkForUpdates(self,win):
        try:
            result = subprocess.run(["flatpak-spawn", "--host", "bash", self.homeFolder + "/.config/ml4w/version/update.sh"], capture_output=True, text=True)
            web_version = result.stdout.strip()

            if (web_version == '0'):
                # print("Show update banner")
                win.update_banner.set_revealed(True)
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/version/update.sh")

    def readDotfilesVersion(self,win):
        self.app_info = json.load(open(self.homeFolder + "/.config/ml4w/version/version.json"))
        try:
            self.app_info = json.load(open(self.homeFolder + "/.config/ml4w/version/version.json"))
            win.ml4w_version.set_text("Version: " + self.app_info["Version"])
            win.ml4w_title.set_text(self.app_info["Title"])
            win.ml4w_subtitle.set_text(self.app_info["Subtitle"])
        except:
            print("ERROR: Could not read the file ~/.config/ml4w/version/name")
            win.ml4w_version.set_text("")
            win.ml4w_title.set_text("ML4W OS")
            win.ml4w_subtitle.set_text("Dotfiles for Hyprland")

    def on_toggle(self, widget, win):
        # Change Label
        if (self.tiling):
            self.btn_toggle.set_icon_name("window-minimize-symbolic")
            self.btn_toggle.set_tooltip_text("Set to tiling")
            self.tiling = False
        else:
            self.btn_toggle.set_icon_name("window-maximize-symbolic")
            self.btn_toggle.set_tooltip_text("Set to floating")
            self.tiling = True

        subprocess.Popen(["hyprctl", "dispatch", "togglefloating", "com.ml4w.welcome"])

    def on_keyboard(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.editor, self.homeFolder + "/.config/hypr/conf/keyboard.conf"])

    def on_shell(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/.config/ml4w/scripts/shell.sh"])

    def on_hyprlandsettings(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "flatpak", "run", "com.ml4w.hyprlandsettings"])

    def on_settings(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "flatpak", "run", "com.ml4w.settings"])

    def on_monitors(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "nwg-displays"])
        self.quit()

    def on_sidebar(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "flatpak", "run", "com.ml4w.sidebar"])

    def on_system_info(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/.config/hypr/scripts/systeminfo.sh"])

    def on_system_update(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/.config/ml4w/scripts/installupdates.sh"])

    def on_uninstall(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.terminal, "--class", "dotfiles-floating", "-e", "ml4w-hyprland-setup", "-m", "uninstall"])

    def on_sddm_wallpaper(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/.config/ml4w/scripts/sddm-wallpaper.sh"])

    def on_nmapplet_start(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "bash", self.homeFolder + "/.config/ml4w/scripts/nm-applet.sh","toggle"])

    def on_keybindings(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "bash", self.homeFolder + "/.config/hypr/scripts/keybindings.sh"])

    def on_wiki(self, widget, _):
        Gtk.UriLauncher(uri="https://mylinuxforwork.github.io/dotfiles/").launch()

    def on_changelog(self, widget, _):
        Gtk.UriLauncher(uri="https://github.com/mylinuxforwork/dotfiles/blob/main/CHANGELOG.md").launch()

    def on_hyprlandhomepage(self, widget, _):
        Gtk.UriLauncher(uri="https://hyprland.org/").launch()

    def on_hyprlandwiki(self, widget, _):
        Gtk.UriLauncher(uri="https://wiki.hyprland.org/").launch()

    def on_wallpapers(self, widget, _):
        Gtk.UriLauncher(uri="https://github.com/mylinuxforwork/wallpaper").launch()

    def on_gitlab(self, widget, _):
        Gtk.UriLauncher(uri="https://github.com/mylinuxforwork/dotfiles").launch()

    def on_howtoupdate(self, widget, _):
        Gtk.UriLauncher(uri="https://mylinuxforwork.github.io/dotfiles/getting-started/update/").launch()

    def on_youtube(self, widget, _):
        Gtk.UriLauncher(uri="https://www.youtube.com/channel/UC0sUzmZ0CHvVCVrpRfGKZfw").launch()

    def on_network(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", self.networkmanager])

    def on_bluetooth(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "blueman-manager"])

    def on_exit_hyprland(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "bash", self.homeFolder + "/.config/hypr/scripts/power.sh exit"])

    def on_autostart(self, widget, _):
        if(self.switch_autostart.get_active()):
            if (os.path.exists(self.homeFolder + "/.cache/ml4w-welcome-autostart")):
                os.remove(self.homeFolder + "/.cache/ml4w-welcome-autostart")
        else:
            file = open(self.homeFolder + "/.cache/ml4w-welcome-autostart", "w+")

    # Callback for the app.about action.
    def on_about_action(self, *args):
        about = Adw.AboutDialog(
            application_name="ML4W Welcome App",
            application_icon='com.ml4w.welcome',
            developer_name="Stephan Raabe",
            version=self.app_info["Version"],
            website="https://github.com/mylinuxforwork/dotfiles-welcome",
            issue_url="https://github.com/mylinuxforwork/dotfiles-welcome/issues",
            support_url="https://github.com/mylinuxforwork/dotfiles-welcome/issues",
            copyright="© 2025 Stephan Raabe",
            license_type=Gtk.License.GPL_3_0_ONLY
        )
        about.present(self.props.active_window)

    # Add an application action.
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

# The application's entry point.
def main(version):
    app = DotfilesWelcomeApplication()
    return app.run(sys.argv)
