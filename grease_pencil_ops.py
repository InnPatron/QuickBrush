import bpy
from .constants import *
from .util import *

def make_grease_pencil_brush_op_idname(i):
    return "quick_brush.grease_pencil_brush_slot{x}".format(x=i + 1)

def make_grease_pencil_brush_op(i):
    def execute(self, context):
        my_data = context.workspace.quick_brush_data.grease_pencil_brush_slots
        (_, slot) = my_data.items()[self.slot]

        n = "NONE"
        if slot.brush != None:
            n = slot.brush.name
            bpy.context.tool_settings.gpencil_paint.brush = slot.brush

        if DEBUG:
            print("Slot {x} in mode {mode} (brush={n})".format(x=self.slot, mode=bpy.context.mode, n=n))
        return {'FINISHED'}

    op_type = type("QuickBrushGreasePencilBrushSlot{x}Op".format(x=i+1), (bpy.types.Operator, ), {
        "bl_idname": make_grease_pencil_brush_op_idname(i),
        "bl_label": "Quick Brush: Grease Pencil Brush Slot {x}".format(x=i+1),
        "slot": i,
        "execute": execute,
    })

    return op_type

class CopyGreasePencilBrushSlotsOp(bpy.types.Operator):
    bl_idname = "quick_brush.copy_grease_pencil_brush_slots"
    bl_label = "Copy Grease Pencil Brush Slots"

    def execute(self, context):
        my_data = context.workspace.quick_brush_data

        if my_data.copy_to_target != None:
            if DEBUG:
                print("Copying to {n}".format(n=my_data.copy_to_target.name))
            destination = my_data.copy_to_target.quick_brush_data.grease_pencil_brush_slots

            try_init_collection(destination, SLOT_COUNT)

            for i in range(0, SLOT_COUNT):
                if my_data.grease_pencil_brush_slots[i] != None:
                    destination[i].brush = my_data.grease_pencil_brush_slots[i].brush
        else:
            self.report({'ERROR'}, "No target workspace")

        return {'FINISHED'}
