import bpy
from .constants import *
from .util import *

class QuickBrushPanel(bpy.types.Panel):
    bl_label = "Quick Brush Workspace Settings"
    bl_idname = "VIEW_3D_PT_QUICK_BRUSH_SETTINGS_LAYOUT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        my_data = context.workspace.quick_brush_data
        layout = self.layout

        r = layout.row()
        r.label(text="Copy To")
        r.template_ID(my_data, "copy_to_target")

class QuickBrushTexturePaintPanel(bpy.types.Panel):
    bl_label = "Texture Paint Settings"
    bl_idname = "VIEW_3D_PT_QUICK_BRUSH_TEXTURE_PAINT_LAYOUT"
    bl_parent_id = "VIEW_3D_PT_QUICK_BRUSH_SETTINGS_LAYOUT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        my_data = context.workspace.quick_brush_data

        try_init_collection(my_data.texture_paint_brush_slots, SLOT_COUNT)

        layout.operator("quick_brush.copy_texture_paint_brush_slots", text="Copy Texture Paint Brushes")

        for i in range(0, SLOT_COUNT):
            r = layout.row()
            c1 = r.column()
            c2 = r.column()
            c2.alignment="CENTER"
            c2.scale_x = 2
            c1.label(text="Slot {x}".format(x=i+1))
            c2.template_ID(my_data.texture_paint_brush_slots[i], "brush")
