#!/bin/bash
cd ..
ARCH=x86_64 appimagetool ml4w-welcome
echo ":: AppImage created"
cp ML4W_Welcome-x86_64.AppImage ~/dotfiles-versions/dotfiles/apps/
echo ":: AppImage copied to ~/dotfiles-versions/dotfiles/apps/"