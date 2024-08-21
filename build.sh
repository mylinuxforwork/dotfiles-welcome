#!/bin/bash
cd ..
ARCH=x86_64 appimagetool dotfiles-welcome
echo ":: AppImage created"
cp ML4W_Welcome-x86_64.AppImage ~/.ml4w-hyprland/dotfiles/share/dotfiles/.config/ml4w/apps/
echo ":: AppImage copied to ~/.ml4w-hyprland/dotfiles/share/dotfiles/.config/ml4w/apps/"