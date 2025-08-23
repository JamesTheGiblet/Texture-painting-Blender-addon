# Blender Addon: Quick Texture Paint Setup

A simple tool to automate the boring parts of texture painting.

The Problem

Setting up an object for texture painting in Blender is a pain. You have to manually unwrap UVs, create a new material, add an image texture node, create a new image file, plug it all together, and then switch to Texture Paint mode. It's about ten clicks every single time you want to start painting. I got tired of it.

The Solution

A simple addon that automates all of that. You select your object, choose a few settings, click one button, and you're instantly in Texture Paint mode, ready to go. It turns a dozen clicks into one.

What It Does

    Auto UV Unwrap: Automaticaly unwraps your mesh using your chosen method (Smart UV Project, etc.).

    Auto Material & Texture: Creates a new material, a new image texture with your specified resolution and base color, and hooks them up correctly.

    Auto Brush Setup: Selects a paint brush and sets its radius and strength to your preference.

    Auto Mode Switch: Drops you directly into Texture Paint Mode so you can start painting immediately.

How to Install It

    Download the .py file.

    In Blender, go to Edit > Preferences > Add-ons.

    Click Install and select the .py file you downloaded.

    Check the box to enable the addon.

How to Use It

    In Object Mode, select the object you want to paint.

    Open the 3D View Sidebar (press 'N') and find the "Texture Paint Setup" panel.

    Adjust the settings like texture name, resolution, and brush size.

    Click the big "Prepare for Texture Paint" button.

That's it. The addon does the rest. You're ready to paint.

Requirements

    Blender 4.1 or newer.

    You must have a mesh object selected in Object Mode.

Recent Upgrades

    v1.2: I added options for base color and different UV unwrap methods. Also, better brush management.

    v1.1: Initial release.

How to Contribute

This is an open project. Feel free to fork the repository, submit pull requests, or report any bugs you find.

License

This addon is licensed under the GPL, just like Blender. It's an open, honest, and free license.

It's a simple tool that saves you a bunch of clicks. The code is the proof that sometimes the best projects are the ones that just fix a simple annoyance.
