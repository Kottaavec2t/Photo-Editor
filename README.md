# Photo Editor
A modern desktop photo editor application built with Python & CustomTkinter.

## Features

- Image Edition
    - Brightness adjustment
    - Grayscale convertion
    - Image rotation

- File Management
    - New blank image creation
    - Import file images
    - Save edited images

- Tools
    - Undo/Redo with history viewer panel
    - Image display with Zoom and Movements
    - Edit panels with sliders and controls

- Customisation
    - Light and Dark themes
    - Widgets themes
    - Panel configuration and Workspace ordering
    - Window geometry automatic save

## Installation

1. Download the project zip file and extract it

2. launch the executable file in dist or the main.py file (depends of version)

## Usage

- Top Bar
    - Import or create an image with folder and plus icons
    - Save your image with the disk icon
    - Zoom with the loops icons
    - Undo/Redo with the arrows icons

- Workspace
    - Look at your image in the photo viewer
    - Move and Zoom to explore
    - Modify your image with the edit panel
    - See your history appear in the history panel

- Parameters
    - To modify your parameters, edit the settings.json file
    - You can then modify panels that are displayed, move the panels size and side, the appearence and the color theme (green, blue and dark-blue)
    - WARNING: DO NOT MODIFY THE fullscreen AND geometry FIELDS

## Requirements

- Python 3.8+
- Pillow (PIL)
- CustomTkinter