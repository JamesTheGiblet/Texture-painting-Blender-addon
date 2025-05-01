bl_info = {
    "name": "Texture Painting Setup",
    "author": "James Gilbert",
    "version": (1, 3),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Texture Paint Setup",
    "description": "Prepares an object for texture painting with UV unwrapping, material creation, texture setup, and brush selection.",
    "category": "Object",
}

import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, EnumProperty, FloatVectorProperty


class OBJECT_OT_PrepareTexturePaint(bpy.types.Operator):
    """Operator to prepare the selected mesh object for texture painting."""
    bl_idname = "object.prepare_texture_paint"
    bl_label = "Prepare for Texture Painting"
    bl_options = {'REGISTER', 'UNDO'}

    # --- Properties for Texture Settings ---
    texture_name: StringProperty(
        name="Texture Name",
        default="Generated_Texture",
        description="Name to give to the new texture image"
    )
    resolution_x: IntProperty(
        name="Resolution X",
        default=1024,
        min=256,
        max=8192,
        description="Width resolution of the new texture image"
    )
    resolution_y: IntProperty(
        name="Resolution Y",
        default=1024,
        min=256,
        max=8192,
        description="Height resolution of the new texture image"
    )
    base_color: FloatVectorProperty(
        name="Base Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),  # Added alpha channel
        size=4,
        min=0.0,
        max=1.0,
        description="Initial RGBA color of the texture image"
    )

    # --- Properties for Material Settings ---
    material_name: StringProperty(
        name="Material Name",
        default="Generated_Material",
        description="Name to give to the new material"
    )

    # --- Properties for UV Unwrap Settings ---
    uv_unwrap_method: EnumProperty(
        name="UV Unwrap",
        items=[
            ('SMART', "Smart UV Project", "Automatically unwrap the mesh"),
            ('LIGHTMAP', "Lightmap Pack", "Create UVs optimized for lightmaps"),
            ('CYLINDER', "Cylinder Unwrap", "Unwrap the mesh as if it were a cylinder"),
        ],
        default='SMART',
        description="Method to use for UV unwrapping"
    )

    # --- Properties for Brush Settings ---
    brush_name: StringProperty(
        name="Brush Name",
        default="Paint",
        description="Name of the brush to select (will create a new one if it doesn't exist)"
    )
    brush_radius: IntProperty(
        name="Brush Radius",
        default=50,
        min=1,
        max=500,
        description="Initial radius of the texture paint brush"
    )
    brush_strength: FloatProperty(
        name="Brush Strength",
        default=0.8,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
        description="Initial strength of the texture paint brush"
    )

    def execute(self, context):
        """Main execution method of the operator."""
        obj = context.object

        # --- Input Validation and Error Handling ---
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object in Object Mode.")
            return {'CANCELLED'}

        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Please ensure you are in Object Mode to run this operator.")
            return {'CANCELLED'}

        # --- Material Handling ---
        try:
            obj.data.materials.clear()
        except Exception as e:
            self.report({'ERROR'}, f"Error clearing existing materials: {e}")
            return {'CANCELLED'}

        # --- UV Unwrap ---
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            if self.uv_unwrap_method == 'SMART':
                bpy.ops.uv.smart_project()
            elif self.uv_unwrap_method == 'LIGHTMAP':
                bpy.ops.uv.lightmap_pack()
            elif self.uv_unwrap_method == 'CYLINDER':
                bpy.ops.uv.unwrap(method='CYLINDER')
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception as e:
            self.report({'ERROR'}, f"Error during UV unwrapping: {e}")
            return {'CANCELLED'}

        # --- Texture Creation ---
        try:
            image = bpy.data.images.new(
                name=self.texture_name,
                width=self.resolution_x,
                height=self.resolution_y,
                color=self.base_color
            )
            if image is None:
                self.report({'ERROR'}, f"Failed to create image texture '{self.texture_name}'.")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error creating image texture: {e}")
            return {'CANCELLED'}

        # --- Material Creation and Node Setup ---
        try:
            material = bpy.data.materials.new(name=self.material_name)
            material.use_nodes = True
            nodes = material.node_tree.nodes

            # Clear default nodes
            for node in list(nodes):
                nodes.remove(node)

            # Add Principled BSDF node
            bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf_node.location = (200, 0)

            # Add texture node
            tex_image_node = nodes.new(type='ShaderNodeTexImage')
            tex_image_node.image = image
            tex_image_node.location = (0, 0)

            # Link texture to Base Color
            material.node_tree.links.new(bsdf_node.inputs['Base Color'], tex_image_node.outputs['Color'])

            # Add Material Output node
            material_output_node = nodes.new(type='ShaderNodeOutputMaterial')
            material_output_node.location = (400, 0)
            material.node_tree.links.new(material_output_node.inputs['Surface'], bsdf_node.outputs['BSDF'])

            # Assign material to object
            obj.data.materials.append(material)

        except Exception as e:
            self.report({'ERROR'}, f"Error creating or setting up the material: {e}")
            # Attempt to remove the created image if material setup failed
            if image:
                bpy.data.images.remove(image)
            return {'CANCELLED'}

        # --- Switch to Texture Paint Mode ---
        try:
            bpy.ops.object.mode_set(mode='TEXTURE_PAINT')
        except Exception as e:
            self.report({'ERROR'}, f"Error switching to Texture Paint mode: {e}")
            return {'CANCELLED'}

        # --- Brush Selection and Setup ---
        try:
            tool_settings = context.tool_settings.image_paint
            brush = bpy.data.brushes.get(self.brush_name)
            if brush is None:
                brush = bpy.data.brushes.new(name=self.brush_name, mode='TEXTURE_PAINT')
                if brush is None:
                    self.report({'ERROR'}, f"Failed to create new brush '{self.brush_name}'.")
                    return {'CANCELLED'}
            tool_settings.brush = brush

            # Set brush properties
            brush.size = self.brush_radius
            brush.strength = self.brush_strength

        except Exception as e:
            self.report({'ERROR'}, f"Error setting up the texture paint brush: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"'{obj.name}' is ready for texture painting with brush '{tool_settings.brush.name}'.")
        return {'FINISHED'}


class VIEW3D_PT_TexturePaintSetup(bpy.types.Panel):
    """Creates a Panel in the 3D View Sidebar for Texture Paint Setup."""
    bl_label = "Texture Paint Setup"
    bl_idname = "VIEW3D_PT_texture_paint_setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Paint Setup"

    def draw(self, context):
        """Draws the panel UI."""
        layout = self.layout
        layout.label(text="Object Preparation", icon='OBJECT_DATA')
        layout.operator("object.prepare_texture_paint", text="Prepare for Texture Paint")

        layout.separator()
        layout.label(text="Texture Settings", icon='IMAGE_DATA')
        layout.prop(context.scene, 'texture_paint_setup_texture_name')
        row = layout.row(align=True)
        row.prop(context.scene, 'texture_paint_setup_resolution_x')
        row.prop(context.scene, 'texture_paint_setup_resolution_y')
        layout.prop(context.scene, 'texture_paint_setup_base_color')

        layout.separator()
        layout.label(text="Material Settings", icon='MATERIAL')
        layout.prop(context.scene, 'texture_paint_setup_material_name')

        layout.separator()
        layout.label(text="UV Unwrap Settings", icon='UV')
        layout.prop(context.scene, 'texture_paint_setup_uv_unwrap_method')

        layout.separator()
        layout.label(text="Brush Settings", icon='BRUSH_DATA')
        layout.prop(context.scene, 'texture_paint_setup_brush_name')
        layout.prop(context.scene, 'texture_paint_setup_brush_radius')
        layout.prop(context.scene, 'texture_paint_setup_brush_strength')


# Store properties in the scene for the panel
def register():
    """Registers the classes and scene properties for the addon."""
    bpy.utils.register_class(OBJECT_OT_PrepareTexturePaint)
    bpy.utils.register_class(VIEW3D_PT_TexturePaintSetup)
    bpy.types.Scene.texture_paint_setup_texture_name = StringProperty(default="Generated_Texture")
    bpy.types.Scene.texture_paint_setup_material_name = StringProperty(default="Generated_Material")
    bpy.types.Scene.texture_paint_setup_resolution_x = IntProperty(default=1024, min=256, max=8192)
    bpy.types.Scene.texture_paint_setup_resolution_y = IntProperty(default=1024, min=256, max=8192)
    bpy.types.Scene.texture_paint_setup_base_color = FloatVectorProperty(subtype='COLOR', default=(1.0, 1.0, 1.0, 1.0), size=4, min=0.0, max=1.0)
    bpy.types.Scene.texture_paint_setup_uv_unwrap_method = EnumProperty(items=[('SMART', "Smart UV Project", "Automatically unwrap the mesh"), ('LIGHTMAP', "Lightmap Pack", "Create UVs optimized for lightmaps"), ('CYLINDER', "Cylinder Unwrap", "Unwrap the mesh as if it were a cylinder")], default='SMART')
    bpy.types.Scene.texture_paint_setup_brush_name = StringProperty(default="Paint")
    bpy.types.Scene.texture_paint_setup_brush_radius = IntProperty(default=50, min=1, max=500)
    bpy.types.Scene.texture_paint_setup_brush_strength = FloatProperty(default=0.8, min=0.0, max=1.0, subtype='FACTOR')


def unregister():
    """Unregisters the classes and removes scene properties."""
    bpy.utils.unregister_class(OBJECT_OT_PrepareTexturePaint)
    bpy.utils.unregister_class(VIEW3D_PT_TexturePaintSetup)
    del bpy.types.Scene.texture_paint_setup_texture_name
    del bpy.types.Scene.texture_paint_setup_material_name
    del bpy.types.Scene.texture_paint_setup_resolution_x
    del bpy.types.Scene.texture_paint_setup_resolution_y
    del bpy.types.Scene.texture_paint_setup_base_color
    del bpy.types.Scene.texture_paint_setup_uv_unwrap_method
    del bpy.types.Scene.texture_paint_setup_brush_name
    del bpy.types.Scene.texture_paint_setup_brush_radius
    del bpy.types.Scene.texture_paint_setup_brush_strength


if __name__ == "__main__":
    register()
