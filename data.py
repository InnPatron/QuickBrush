import bpy

class QuickBrushProperties(bpy.types.PropertyGroup):
    columns: bpy.props.IntProperty(
        name = "Test Int Property"
    )

class QuickBrushPanel(bpy.types.Panel):
    bl_label = "Quick Brush Workspace Settings"
    bl_idname = "VIEW_3D_PT_QUICK_BRUSH_SETTINGS_LAYOUT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        my_data = context.workspace.quick_brush_data

        layout.prop(my_data, "columns")
        layout.separator()
