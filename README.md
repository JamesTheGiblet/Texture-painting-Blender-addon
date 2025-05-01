# Texture Painting Setup Addon for Blender

_A Blender addon to streamline the texture painting workflow with automated UV mapping, material creation, texture setup, and brush selection._

## Features
- **Automated UV Mapping:** Choose from Smart UV Project, Lightmap Pack, or Cylinder Unwrap methods.
- **Customizable Textures:** Define resolution, base color (RGBA), and texture name.
- **Material Setup:** Automatically create and assign a material with texture nodes.
- **Brush Selection:** Auto-select or create a brush with user-defined radius and strength values.
- **Efficient Workflow:** Jump straight into Texture Paint Mode with everything set up.

## Installation
1. Download the addon as a `.py` file from this repository.
2. Open Blender and go to **Edit > Preferences > Add-ons**.
3. Click **Install**, locate the `.py` file, and enable the addon.
4. Access the addon panel in the 3D View Sidebar under **Texture Paint Setup**.

## Usage
1. Select the object you want to prepare for texture painting.
2. Open the addon panel in the 3D View Sidebar.
3. Customize the settings for:
   - **Texture Name**
   - **Material Name**
   - **Resolution (X and Y)**
   - **Base Color (RGBA)**
   - **UV Unwrap Method**
   - **Brush Name, Radius, and Strength**
4. Click **Prepare for Texture Paint**.
5. Blender will:
   - Clear existing materials from the selected object.
   - Apply the selected UV unwrapping method.
   - Create a new image texture and material.
   - Switch to Texture Paint Mode.
   - Select or create the specified brush.

You're now ready to start texture painting immediately!

## Requirements
- Blender 4.4 or later.
- A mesh object selected in **Object Mode**.

## Examples
### Before:
- An unwrapped object with no materials or textures.

### After:
- The object is UV-mapped, has a material with a texture, and is ready for painting with a predefined brush.

## Changelog
### Version 1.2
- Added support for customizable base colors and UV unwrap methods.
- Enhanced brush management with auto-selection and customization.
- Improved user interface in the 3D View Sidebar.

## License
This addon is licensed under the **GPL v3.0**, in compliance with Blender's licensing. See the `LICENSE` file for more details.

## Contributions
Contributions are welcome! Feel free to fork this repository, submit pull requests, or report issues.

## Contact
For inquiries, feedback, or collaboration opportunities, reach out via GitHub.

---
