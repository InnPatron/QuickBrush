bl_info = {
    "name": "Quick Brush",
    "description": "Set up keybindings for brushes",
    "blender": (3, 4, 0),
    "category": "3D View",
}

import bpy
from .settings_ui import *
from .data import *
from .constants import *
from .ops import *

registered = []
image_paint_keymap_items = []

def register_texture_paint_brush_slot_ops(n):
    for i in range(0, n):
        op_type = make_texture_brush_op(i)
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
            kmi = km.keymap_items.new(make_texture_paint_brush_op_idname(i), 'NONE', 'PRESS')
            image_paint_keymap_items.append(kmi)

def unregister_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Unregister texture paint bindings
        km = kc.keymaps["Image Paint"]
        for kmi in km.keymap_items:
            if kmi in image_paint_keymap_items:
                km.keymap_items.remove(kmi)

def unregister_ops():
    for r in registered:
        bpy.utils.unregister_class(r)

def register():
    register_texture_paint_brush_slot_ops(SLOT_COUNT)
    register_keymaps(SLOT_COUNT)

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

