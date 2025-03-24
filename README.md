# ML4W Dotfiles Welcome App

After starting the ML4W Dotfiles for Hyprland for the first time, the ML4W Welcome App appears. This app is the starting point to discover the Hyprland configuration.

The welcome screen includes the most important keybindings to open a terminal or a browser.

You can start the ML4W Welcome App by clicking on the L icon on the right side in waybar or be entering ml4w in your terminal (if you're using the .bashrc from the dotfiles).

In the Settings Menu you can access the following functions:

- Update Wallpaper: Opens the wallpaper selector
- Change Waybar Theme: Opens the waybar theme switcher and gives access to the available themes for the waybar status bar
- Change GTK Theme: Opens nwg-look to select the theme for GTK 3 applications incl. widgets, icons and cursors
- Refresh GTK Settings: Reloads the Hyprland GTK configuration (required when changing the mouse cursor)
- Hyprland Settings: Opens the Hyprland Settings script to customize the look and feel, environment variables, monitor resolution, etc.
- Network Settings: Select your network configuration incl. WiFi
- Update your System: Starts the terminal application to update your Arch packages (pacman & yay)
- Cleanup your System: Removes old orphans and cached files generated during previous installations
- Reload Waybar: Reloads the waybar
- Toggle Waybar: You can hide or show waybar when you want to try our other status bars.

The ML4W Welcome App starts several scripts from the ML4W dotfiles:
https://github.com/mylinuxforwork/dotfiles

You can find the sourcecode of the ML4W Welcome App in this repository:
https://github.com/mylinuxforwork/dotfiles-welcome

## Installation

Copy the following command into your terminal.

```
curl -s https://raw.githubusercontent.com/mylinuxforwork/packages-installer/main/setup.sh | bash -s -- -p flatpak -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-welcome/master/com.ml4w.welcome.pkginst com.ml4w.welcome
```
> The installation is build with ML4W Packages Installer. https://github.com/mylinuxforwork/packages-installer

## Uninstall

```
flatpak uninstall com.ml4w.welcome
```

## GTK Development Resources 

GTK Tutorial:
https://developer.gnome.org/documentation/tutorials/beginners.html

GTK Python Tutorial: 
https://github.com/Taiko2k/GTK4PythonTutorial

GTK Python Examples:
https://github.com/natorsc/py-gtk

Workbench:
https://flathub.org/apps/re.sonny.Workbench

Icon Library:
https://flathub.org/apps/org.gnome.design.IconLibrary

AppImage Tool:
https://appimage.github.io/appimagetool/


