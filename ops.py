import bpy
from .constants import *

def make_texture_paint_brush_op_idname(i):
    return "quick_brush.texture_paint_brush_slot{x}".format(x=i + 1)

def make_texture_brush_op(i):
    def execute(self, context):
        my_data = context.workspace.quick_brush_data.texture_paint_brush_slots
        (_, slot) = my_data.items()[self.slot]

        n = "NONE"
        if slot.brush != None:
            n = slot.brush.name
            bpy.context.tool_settings.image_paint.brush = slot.brush

        if DEBUG:
            print("Slot {x} in mode {mode} (brush={n})".format(x=self.slot, mode=bpy.context.mode, n=n))
        return {'FINISHED'}

    op_type = type("QuickBrushTexturePaintBrushSlot{x}Op".format(x=i+1), (bpy.types.Operator, ), {
        "bl_idname": make_texture_paint_brush_op_idname(i),
        "bl_label": "Quick Brush: Paint Brush Slot {x}".format(x=i+1),
        "slot": i,
        "execute": execute,
    })

    return op_type
