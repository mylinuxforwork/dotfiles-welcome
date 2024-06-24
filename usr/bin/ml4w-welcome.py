#  __  __ _    _  ___        __     _    _                 _   
# |  \/  | |  | || \ \      / /    / \  | |__   ___  _   _| |_ 
# | |\/| | |  | || |\ \ /\ / /    / _ \ | '_ \ / _ \| | | | __|
# | |  | | |__|__   _\ V  V /    / ___ \| |_) | (_) | |_| | |_ 
# |_|  |_|_____| |_|  \_/\_/    /_/   \_\_.__/ \___/ \__,_|\__|
                                                             
import sys
import gi
import subprocess
import os
import threading
import shutil

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
from gi.repository import GLib
from gi.repository import GObject

# Get script path
pathname = os.path.dirname(sys.argv[0])    

# -----------------------------------------
# Define UI template
# -----------------------------------------
@Gtk.Template(filename = pathname + '/src/welcome.ui')

# -----------------------------------------
# Main Window
# -----------------------------------------
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'Ml4wWelcomeWindow'

    # Get objects from template
    ml4w_version = Gtk.Template.Child()
    ml4w_logo = Gtk.Template.Child()
    update_banner = Gtk.Template.Child()
    btn_toggle = Gtk.Template.Child()
    switch_autostart = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -----------------------------------------
# Main App
# -----------------------------------------
class MyApp(Adw.Application):

    # Path to home folder
    homeFolder = os.path.expanduser('~')
    pathname = os.path.dirname(sys.argv[0]) 
    current_version_name = ""
    current_version_code = ""
    tiling = False
    browser = "chromium"
    terminal = "alacritty"
    editor = "mousepad"
    filemanager = "thunar"
    win = Adw.ApplicationWindow()

    def __init__(self, **kwargs):
        super().__init__(application_id='com.ml4w.welcome', flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('update', self.on_system_update)
        self.create_action('pacman', self.on_pacman)
        self.create_action('cleanup', self.on_system_cleanup)
        self.create_action('about', self.on_about)
        self.create_action('settings', self.on_settings)
        self.create_action('hyprlandsettings', self.on_hyprlandsettings)
        self.create_action('waybar_reload', self.on_waybar_reload)
        self.create_action('keybindings', self.on_keybindings)
        self.create_action('gitlab', self.on_gitlab)
        self.create_action('youtube', self.on_youtube)
        self.create_action('wallpaper', self.on_wallpaper)
        self.create_action('wallpaper_folder', self.on_wallpaper_folder)
        self.create_action('network', self.on_network)
        self.create_action('bluetooth', self.on_bluetooth)
        self.create_action('waybartheme', self.on_waybartheme)
        self.create_action('gtktheme', self.on_gtktheme)
        self.create_action('gtkrefresh', self.on_gtkrefresh)
        self.create_action('howtoupdate', self.on_howtoupdate)
        self.create_action('toggle', self.on_toggle)
        self.create_action('autostart', self.on_autostart)
        self.create_action('hyprlandhomepage', self.on_hyprlandhomepage)
        self.create_action('hyprlandwiki', self.on_hyprlandwiki)
        self.create_action('systeminfo', self.on_system_info)
        self.create_action('unlock', self.on_system_unlock)
        self.create_action('timeshift', self.on_system_timeshift)
        self.create_action('thunarterminal', self.on_system_thunarterminal)
        self.create_action('sddm_wallpaper', self.on_sddm_wallpaper)
        self.create_action('sddm_enable', self.on_sddm_enable)
        self.create_action('sddm_disable', self.on_sddm_disable)
        self.create_action('exit_hyprland', self.on_exit_hyprland)
        self.create_action('update_dotfiles', self.on_update_dotfiles)
        self.create_action('keyboard', self.on_keyboard)
        self.create_action('changelog', self.on_changelog)
        self.create_action('wiki', self.on_wiki)
        self.create_action('diagnosis', self.on_diagnosis)
        self.create_action('uninstall', self.on_uninstall)
        self.create_action('nm-applet-start', self.on_nmapplet_start)
        self.create_action('nm-applet-stop', self.on_nmapplet_stop)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        # Get Autostart Button
        self.switch_autostart = win.switch_autostart
        if (os.path.exists(self.homeFolder + "/.cache/ml4w-welcome-autostart")):
            self.switch_autostart.set_active(False)
        else:
            self.switch_autostart.set_active(True)

        # Get Window Toggle Button
        self.btn_toggle = win.btn_toggle

        # Set ML4W logo
        win.ml4w_logo.set_from_file(pathname + "/src/icon.png")

        # Check dotfiles version
        self.readDotfilesVersion(win)

        # Force dark theme
        # self.changeTheme(win)

        # Check for updates
        self.checkForUpdates(win)

        # get Browser
        self.getBrowser()

        # get Terminal
        self.getTerminal()

        # get Editor
        self.getEditor()

        # get Filemanager
        self.getFilemanager()

        # Show Application Window
        win.present()

        print (":: Welcome to ML4W Welcome App")

    def changeTheme(self,win):
        app = win.get_application()
        sm = app.get_style_manager()
        sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

    def getTerminal(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/dotfiles/.settings/terminal.sh"], capture_output=True, text=True)
            self.terminal = result.stdout.strip()
            print (":: Using Terminal " + self.terminal)
        except:
            print("ERROR: Could not read the file /dotfiles/.settings/terminal.sh")

    def getBrowser(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/dotfiles/.settings/browser.sh"], capture_output=True, text=True)
            self.browser = result.stdout.strip()
            print (":: Using Browser " + self.browser)
        except:
            print("ERROR: Could not read the file /dotfiles/.settings/browser.sh")

    def getEditor(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/dotfiles/.settings/editor.sh"], capture_output=True, text=True)
            self.editor = result.stdout.strip()
            print (":: Using Editor " + self.editor)
        except:
            print("ERROR: Could not read the file /dotfiles/.settings/editor.sh")

    def getFilemanager(self):
        try:
            result = subprocess.run(["cat", self.homeFolder + "/dotfiles/.settings/filemanager.sh"], capture_output=True, text=True)
            self.filemanager = result.stdout.strip()
            print (":: Using Filemanager " + self.filemanager)
        except:
            print("ERROR: Could not read the file /dotfiles/.settings/filemanager.sh")

    def on_update_dotfiles(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/update.sh"])

    def checkForUpdates(self,win):
        try:
            result = subprocess.run(["bash", self.homeFolder + "/dotfiles/.version/update.sh"], capture_output=True, text=True)
            web_version = result.stdout.strip()
            # print("Update " +  web_version)

            if (web_version == '0'):
                # print("Show update banner")
                win.update_banner.set_revealed(True)
        except:
            print("ERROR: Could not read the file /dotfiles/.version/update.sh")

    def readDotfilesVersion(self,win):
        try:
            result = subprocess.run(["bash", self.homeFolder + "/dotfiles/.version/version.sh"], capture_output=True, text=True)
            # print("Version " +  result.stdout)
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
            application_name="ML4W Welcome App",
            developer_name="Stephan Raabe",
            version="2.9.1",
            website="https://gitlab.com/stephan-raabe/dotfiles",
            issue_url="https://gitlab.com/stephan-raabe/dotfiles/-/issues",
            support_url="https://gitlab.com/stephan-raabe/dotfiles/-/issues",
            copyright="© 2024 Stephan Raabe",
            license_type=Gtk.License.GPL_3_0_ONLY
        )
        dialog.present()

    # Toggle floating of welcome app
    # hyprctl dispatch togglefloating com.ml4w.welcome

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
        subprocess.Popen([self.editor, self.homeFolder + "/dotfiles/hypr/conf/keyboard.conf"])

    def on_hyprlandsettings(self, widget, _):
        subprocess.Popen([self.homeFolder + "/dotfiles/apps/ML4W_Hyprland_Settings-x86_64.AppImage"])

    def on_settings(self, widget, _):
        subprocess.Popen([self.homeFolder + "/dotfiles/apps/ML4W_Dotfiles_Settings-x86_64.AppImage"])

    def on_system_info(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "--hold", "-e", self.pathname + "/src/scripts/systeminfo.sh"])

    def on_diagnosis(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/hypr/scripts/diagnosis.sh"])

    def on_system_update(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/installupdates.sh"])

    def on_pacman(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/pacman.sh"])

    def on_uninstall(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/uninstall.sh"])

    def on_system_timeshift(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/installtimeshift.sh"])

    def on_system_thunarterminal(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/thunarterminal.sh"])

    def on_system_unlock(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/unlock-pacman.sh"])

    def on_system_cleanup(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/scripts/cleanup.sh"])

    def on_sddm_wallpaper(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/sddm/scripts/wallpaper.sh"])

    def on_sddm_disable(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/sddm/scripts/disable.sh"])

    def on_sddm_enable(self, widget, _):
        subprocess.Popen([self.terminal, "--class", "dotfiles-floating", "-e", self.homeFolder + "/dotfiles/sddm/scripts/enable.sh"])

    def on_nmapplet_start(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/scripts/nm-applet.sh"])

    def on_nmapplet_stop(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/scripts/nm-applet.sh","stop"])

    def on_waybar_reload(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/waybar/launch.sh"])

    def on_keybindings(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/hypr/scripts/keybindings.sh"])

    def on_wiki(self, widget, _):
        subprocess.Popen([self.browser, "https://gitlab.com/stephan-raabe/dotfiles/-/wikis/home"])

    def on_changelog(self, widget, _):
        subprocess.Popen([self.browser, "https://gitlab.com/stephan-raabe/dotfiles/-/blob/main/CHANGELOG.md"])

    def on_hyprlandhomepage(self, widget, _):
        subprocess.Popen([self.browser, "https://hyprland.org/"])

    def on_hyprlandwiki(self, widget, _):
        subprocess.Popen([self.browser, "https://wiki.hyprland.org/"])

    def on_gitlab(self, widget, _):
        subprocess.Popen([self.browser, "https://gitlab.com/stephan-raabe/dotfiles"])

    def on_howtoupdate(self, widget, _):
        subprocess.Popen([self.browser, "https://gitlab.com/stephan-raabe/dotfiles#update-with-git"])
        
    def on_youtube(self, widget, _):
        subprocess.Popen([self.browser, "https://www.youtube.com/channel/UC0sUzmZ0CHvVCVrpRfGKZfw"])

    def on_wallpaper(self, widget, _):
        subprocess.Popen(["waypaper")

    def on_wallpaper_folder(self, widget, _):
        subprocess.Popen([self.filemanager, self.homeFolder + "/wallpaper/"])

    def on_waybartheme(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/waybar/themeswitcher.sh"])

    def on_network(self, widget, _):
        subprocess.Popen(["nm-connection-editor"])

    def on_bluetooth(self, widget, _):
        subprocess.Popen(["overskride"])

    def on_gtktheme(self, widget, _):
        subprocess.Popen(["nwg-look"])

    def on_gtkrefresh(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/hypr/scripts/gtk.sh"])

    def on_exit_hyprland(self, widget, _):
        subprocess.Popen(["bash", self.homeFolder + "/dotfiles/hypr/scripts/power.sh exit"])

    def on_autostart(self, widget, _):
        if(self.switch_autostart.get_active()):
            if (os.path.exists(self.homeFolder + "/.cache/ml4w-welcome-autostart")):
                os.remove(self.homeFolder + "/.cache/ml4w-welcome-autostart")
        else:
            file = open(self.homeFolder + "/.cache/ml4w-welcome-autostart", "w+")

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
sm = app.get_style_manager()
sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
app.run(sys.argv)