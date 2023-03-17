import bpy

bl_info = {
    "name": "Quick Brush",
    "description": "Set up keybindings for brushes",
    "blender": (3, 4, 0),
    "category": "3D View",
}

from .data import *

# Config
paint_brush_slot_count = 10

# Internals
registered = []
keymap_items = []

def make_paint_brush_op_idname(i):
    return "quick_brush.paint_brush_slot{x}".format(x=i + 1)

def register_texture_paint_brush_slot_ops(n):
    for i in range(0, n):
        def execute(self, context):
            my_data = context.workspace.quick_brush_data.texture_paint_brush_slots
            (_, slot) = my_data.items()[self.slot]

            n = "NONE"
            if slot.brush != None:
                n = slot.brush.name
                bpy.context.tool_settings.image_paint.brush = slot.brush

            print("Slot {x} in mode {mode} (brush={n})".format(x=self.slot, mode=bpy.context.mode, n=n))
            return {'FINISHED'}

        op_type = type("QuickBrushPaintBrushSlot{x}Op".format(x=i+1), (bpy.types.Operator, ), {
            "bl_idname": make_paint_brush_op_idname(i),
            "bl_label": "Quick Brush: Paint Brush Slot {x}".format(x=i+1),
            "slot": i,
            "execute": execute,
        })

        bpy.utils.register_class(op_type)
        registered.append(op_type)

# source: https://blenderartists.org/t/how-to-create-a-shortcut-for-a-custom-script/545177
def register_keymaps(paint_brush_slots):
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Register texture paint bindings
        if "Image Paint" not in kc.keymaps:
            kc.keymaps.new(name="Image Paint", space_type="EMPTY")
        km = kc.keymaps["Image Paint"]
        for i in range(0, paint_brush_slots):
            kmi = km.keymap_items.new(make_paint_brush_op_idname(i), 'NONE', 'PRESS')
            keymap_items.append(kmi)

def unregister_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Unregister texture paint bindings
        km = kc.keymaps["Image Paint"]
        for kmi in km.keymap_items:
            if kmi in keymap_items:
                km.keymap_items.remove(kmi)

def unregister_ops():
    for r in registered:
        bpy.utils.unregister_class(r)

def register():
    register_texture_paint_brush_slot_ops(paint_brush_slot_count)
    register_keymaps(paint_brush_slot_count)

    bpy.utils.register_class(QuickBrushTexturePaintSlot)
    bpy.utils.register_class(QuickBrushProperties)
    bpy.utils.register_class(QuickBrushPanel)
    bpy.utils.register_class(QuickBrushTexturePaintPanel)
    bpy.types.WorkSpace.quick_brush_data = bpy.props.PointerProperty(type=QuickBrushProperties)

def unregister():
    unregister_keymaps()
    unregister_ops()

    bpy.utils.unregister_class(QuickBrushPanel)
    bpy.utils.unregister_class(QuickBrushProperties)
    bpy.utils.unregister_class(QuickBrushTexturePaintSlot)
    bpy.utils.unregister_class(QuickBrushTexturePaintPanel)
    del bpy.types.WorkSpace.quick_brush_data

if __name__ == "__main__":
    register()

